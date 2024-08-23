from PartA import basic
import PartA.Lexen


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
        return basic.RTResult().success(
            basic.Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = basic.RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(basic.RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = basic.RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = basic.RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == PartA.Lexen.TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == PartA.Lexen.TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == PartA.Lexen.TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == PartA.Lexen.TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == PartA.Lexen.TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == PartA.Lexen.TT_MODULO:
            result, error = left.moded_by(right)
        elif node.op_tok.type == PartA.Lexen.TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == PartA.Lexen.TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == PartA.Lexen.TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == PartA.Lexen.TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == PartA.Lexen.TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == PartA.Lexen.TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(PartA.Lexen.TT_KEYWORD, 'AND') or node.op_tok.type == PartA.Lexen.TT_AND:
            result, error = left.anded_by(right)
        elif node.op_tok.matches(PartA.Lexen.TT_KEYWORD, 'OR') or node.op_tok.type == PartA.Lexen.TT_OR:
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = basic.RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_tok.type == PartA.Lexen.TT_MINUS:
            number, error = number.multed_by(basic.Number(-1))
        elif node.op_tok.matches(PartA.Lexen.TT_KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = basic.RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_value)

        return res.success(None)

    def visit_FuncDefNode(self, node, context):
        res = basic.RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = basic.Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start,
                                                                                                  node.pos_end)

        # Store function in the symbol table
        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = basic.RTResult()
        args = []

        # Get the value to call (function or lambda)
        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        # Evaluate arguments
        for arg_node in node.arg_nodes:
            arg_value = res.register(self.visit(arg_node, context))
            if res.error: return res
            args.append(arg_value)

        # Handle function or lambda call
        if isinstance(value_to_call, basic.Function):
            return_value = res.register(value_to_call.execute(args))
            if res.error: return res
            return res.success(return_value)

        elif isinstance(value_to_call, basic.Lambda):
            # Check if the number of arguments matches the number of parameters
            if len(args) != len(value_to_call.param_names):
                return res.failure(basic.RTError(
                    node.pos_start, node.pos_end,
                    f"Lambdas take exactly {len(value_to_call.param_names)} arguments",
                    context
                ))
            return_value = res.register(value_to_call.execute(args))
            if res.error: return res
            return res.success(return_value)

        else:
            return res.failure(basic.RTError(
                node.pos_start, node.pos_end,
                "Can only call functions or lambdas",
                context
            ))

    def visit_LambdaNode(self, node, context):
        return basic.RTResult().success(
            basic.Lambda(node.param_names, node.body_node).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
