import Lexen
from Common import Number, RTResult, RTError
from Function import Function, String, List


#######################################
# CONTEXT
#######################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None


#######################################
# SYMBOL TABLE
#######################################

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


#######################################
# INTERPRETER
#######################################

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################

    def visit_NumberNode(self, node, context):
        return Lexen.RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error: return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = Lexen.RTResult()

        # Evaluate left and right nodes
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        # Handle different operations based on the operator token type
        if node.op_tok.type == Lexen.TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == Lexen.TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == Lexen.TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == Lexen.TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == Lexen.TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == Lexen.TT_MODULO:
            result, error = left.moded_by(right)
        elif node.op_tok.type == Lexen.TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == Lexen.TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == Lexen.TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == Lexen.TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == Lexen.TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.type == Lexen.TT_OR:
            result, error = left.ored_by(right)
        elif node.op_tok.type == Lexen.TT_AND:
            result, error = left.anded_by(right)
        elif node.op_tok.matches(Lexen.TT_KEYWORD, 'AND'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(Lexen.TT_KEYWORD, 'OR'):
            result, error = left.ored_by(right)
        else:
            return res.failure(Lexen.InvalidSyntaxError(
                node.pos_start, node.pos_end,
                "Invalid operator"
            ))

        # Return the result or an error
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_tok.type == Lexen.TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(Lexen.TT_KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(Number.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.error: return res
            return res.success(Number.null if should_return_null else expr_value)

        return res.success(Number.null)

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_return_null).set_context(context).set_pos(node.pos_start,
                                                                                            node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        return res.success(return_value)


class Boolean:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __bool__(self):
        return self.value
