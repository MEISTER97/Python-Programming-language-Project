from PartA import basic
import PartA.Lexen


#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.result = None
        self.last_registered_advance_count = 0
        self.advance_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != PartA.Lexen.TT_EOF:
            return res.failure(basic.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', '<=', '>=', 'AND(&&)', or 'OR(||)'"
            ))
        return res

    def parse_lambda_expr(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        # Check if the current token is 'LAMBDA' or 'λ'
        if self.current_tok.matches(PartA.Lexen.TT_KEYWORD, 'LAMBDA') or self.current_tok.matches(
                PartA.Lexen.TT_KEYWORD, 'λ'):
            self.advance()
        else:
            return res.failure(
                basic.InvalidSyntaxError(pos_start, self.current_tok.pos_end, "Expected 'LAMBDA' or 'λ'"))

        param_names = []

        # Parse parameters (multiple parameters separated by commas)
        while self.current_tok.type == PartA.Lexen.TT_IDENTIFIER:
            param_names.append(self.current_tok.value)
            self.advance()

            # Check if the next token is a comma or dot
            if self.current_tok.type == PartA.Lexen.TT_COMMA:
                self.advance()
            elif self.current_tok.type == PartA.Lexen.TT_DOT:
                self.advance()
                break
            else:
                return res.failure(basic.InvalidSyntaxError(pos_start, self.current_tok.pos_end, "Expected ',' or '.'"))

        # Ensure at least one parameter is provided
        if not param_names:
            return res.failure(
                basic.InvalidSyntaxError(pos_start, self.current_tok.pos_end, "Expected at least one identifier"))

        # Parse the body of the lambda expression
        expr_result = self.expr()  # Ensure that `self.expr()` correctly parses the body expression
        if expr_result.error:
            return res.failure(expr_result.error)

        body_node = expr_result.node

        # Return a LambdaNode with parameters and body
        return res.success(basic.LambdaNode(param_names, body_node, pos_start, self.current_tok.pos_end.copy()))

    ###################################

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(PartA.Lexen.TT_KEYWORD, 'IF'):
            return res.failure(basic.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'IF'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(PartA.Lexen.TT_KEYWORD, 'THEN'):
            return res.failure(basic.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))

        while self.current_tok.matches(PartA.Lexen.TT_KEYWORD, 'ELIF'):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error: return res

            if not self.current_tok.matches(PartA.Lexen.TT_KEYWORD, 'THEN'):
                return res.failure(basic.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'THEN'"
                ))

            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error: return res
            cases.append((condition, expr))

        if self.current_tok.matches(PartA.Lexen.TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expr())
            if res.error: return res

        return res.success(basic.IfNode(cases, else_case))

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        # Check for lambda expressions first
        if tok.matches(PartA.Lexen.TT_KEYWORD, 'LAMBDA') or tok.matches(PartA.Lexen.TT_KEYWORD, 'λ'):
            lambda_expr = res.register(self.parse_lambda_expr())
            if res.error: return res
            return res.success(lambda_expr)

        elif tok.type in (PartA.Lexen.TT_INT, PartA.Lexen.TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(basic.NumberNode(tok))

        elif tok.type == PartA.Lexen.TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(basic.VarAccessNode(tok))

        elif tok.type == PartA.Lexen.TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == PartA.Lexen.TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(basic.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        elif tok.matches(PartA.Lexen.TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(PartA.Lexen.TT_KEYWORD, 'FUNC'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(basic.InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, identifier, '+', '-', '(', 'IF', 'FUNC', or 'LAMBDA'"
        ))

    def power(self):
        return self.bin_op(self.call, (PartA.Lexen.TT_POW,), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (PartA.Lexen.TT_PLUS, PartA.Lexen.TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(basic.UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (PartA.Lexen.TT_MUL, PartA.Lexen.TT_DIV, PartA.Lexen.TT_MODULO))

    def arith_expr(self):
        return self.bin_op(self.term, (PartA.Lexen.TT_PLUS, PartA.Lexen.TT_MINUS))

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(PartA.Lexen.TT_KEYWORD, 'NOT'):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(basic.UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (PartA.Lexen.TT_EE, PartA.Lexen.TT_NE, PartA.Lexen.TT_LT,
                                                          PartA.Lexen.TT_GT, PartA.Lexen.TT_LTE, PartA.Lexen.TT_GTE)))

        if res.error:
            return res.failure(basic.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected int, float, identifier, '+', '-', '(' or 'NOT'"
            ))

        return res.success(node)

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(PartA.Lexen.TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != PartA.Lexen.TT_IDENTIFIER:
                return res.failure(basic.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != PartA.Lexen.TT_EQ:
                return res.failure(basic.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(basic.VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((PartA.Lexen.TT_KEYWORD, 'AND'), (PartA.Lexen.TT_KEYWORD,
                                                                                           'OR'), PartA.Lexen.TT_AND,
                                                         PartA.Lexen.TT_OR)))

        if res.error:
            return res.failure(basic.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'VAR', 'IF', 'FOR', 'WHILE', 'FUNC', int, float, identifier, '+', '-', '(' or 'NOT'"
            ))

        return res.success(node)

    def parse_call_expr(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        # Parse the function (lambda or other callable)
        func_expr = res.register(self.expr())
        if res.error: return res

        # Parse the arguments
        args = []
        if self.current_tok.type == PartA.Lexen.TT_LPAREN:
            self.advance()
            if self.current_tok.type != PartA.Lexen.TT_RPAREN:
                args.append(res.register(self.expr()))
                if res.error: return res
                while self.current_tok.type == PartA.Lexen.TT_COMMA:
                    self.advance()
                    args.append(res.register(self.expr()))
                    if res.error: return res
            if self.current_tok.type != PartA.Lexen.TT_RPAREN:
                return res.failure(basic.InvalidSyntaxError(pos_start, self.current_tok.pos_end, "Expected ')'"))
            self.advance()

        return res.success(basic.CallNode(func_expr, args, pos_start, self.current_tok.pos_end.copy()))

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res

        if self.current_tok.type == PartA.Lexen.TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == PartA.Lexen.TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(basic.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUNC', int, float, identifier, '+', '-', '(' or 'NOT'"
                    ))

                while self.current_tok.type == PartA.Lexen.TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_tok.type != PartA.Lexen.TT_RPAREN:
                    return res.failure(basic.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()
            return res.success(basic.CallNode(atom, arg_nodes))
        return res.success(atom)

    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(PartA.Lexen.TT_KEYWORD, 'FUNC'):
            return res.failure(basic.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'FUNC'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == PartA.Lexen.TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != PartA.Lexen.TT_LPAREN:
                return res.failure(basic.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '('"
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != PartA.Lexen.TT_LPAREN:
                return res.failure(basic.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or '('"
                ))

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == PartA.Lexen.TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == PartA.Lexen.TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != PartA.Lexen.TT_IDENTIFIER:
                    return res.failure(basic.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != PartA.Lexen.TT_RPAREN:
                return res.failure(basic.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.current_tok.type != PartA.Lexen.TT_RPAREN:
                return res.failure(basic.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or ')'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != PartA.Lexen.TT_ARROW:
            return res.failure(basic.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '->'"
            ))

        res.register_advancement()
        self.advance()
        node_to_return = res.register(self.expr())
        if res.error: return res

        return res.success(basic.FuncDefNode(
            var_name_tok,
            arg_name_toks,
            node_to_return
        ))

    ###################################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = basic.BinOpNode(left, op_tok, right)

        return res.success(left)
