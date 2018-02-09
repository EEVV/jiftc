from parser.lexer.token import TokenType
from parser.lexer import Lexer, error
from parser.node import *


class Parser:
	def __init__(self, source):
		self.lexer = Lexer(source)

		self.reset()

	def reset(self):
		self.token = None
		self.lexer.reset()

	def advance(self):
		lexeme = self.token

		self.token = self.lexer.get_token()

		return lexeme

	def skip_newlines(self):
		while self.token.type == TokenType.NEWLINE:
			self.advance()

	def parse_anon_field(self):
		result = Field(None, None)

		if self.token.type == TokenType.IDENTIFIER:
			result.name = self.advance()

		if self.token.type in [TokenType.TYPE_IDENTIFIER, TokenType.LEFT_CURLY_BRACKET]:
			result.type = self.parse_type()

		return result

	def parse_type_struct(self):
		if self.token.type != TokenType.LEFT_CURLY_BRACKET:
			error.highlight(self.token.position)
			print("Error: expected a `{` while parsing struct type")
			exit()

		result = StructTypeNode([self.advance()], [])

		self.skip_newlines()

		if self.token.type != TokenType.RIGHT_CURLY_BRACKET:
			result.fields.append(self.parse_anon_field())

		while self.token.type in [TokenType.COMMA, TokenType.NEWLINE]:
			self.advance()
			self.skip_newlines()

			if self.token.type == TokenType.RIGHT_CURLY_BRACKET:
				break

			result.fields.append(self.parse_anon_field())

		if self.token.type != TokenType.RIGHT_CURLY_BRACKET:
			error.highlight(self.token.position)
			print("Error: expected a `}` while parsing struct type")
			exit()

		result.tokens.append(self.advance())

		return result

	def parse_type_array(self):
		if self.token.type != TokenType.LEFT_SQUARE_BRACKET:
			error.highlight(self.token.position)
			print("Error: expected a `[` while parsing array type")
			exit()

		result =  ArrayTypeNode([self.advance()], self.parse_type())

		if self.token.type != TokenType.RIGHT_SQUARE_BRACKET:
			error.highlight(self.token.position)
			print("Error: expected a `]` while parsing array type")
			exit()

		result.tokens.append(self.advance())

		return result

	def parse_type(self):
		if self.token.type == TokenType.TYPE_IDENTIFIER:
			return IdenTypeNode([self.advance()])
		if self.token.type == TokenType.LEFT_SQUARE_BRACKET:
			return self.parse_type_array()
		if self.token.type == TokenType.LEFT_CURLY_BRACKET:
			return self.parse_type_struct()

	# factor ::= number | identifier | array
	def parse_factor(self):
		if self.token.type == TokenType.NUMBER:
			result = NumNode([self.advance()])
		elif self.token.type == TokenType.IDENTIFIER:
			result = IdenNode([self.advance()])
		elif self.token.type == TokenType.LEFT_SQUARE_BRACKET:
			result = self.parse_array()
		elif self.token.type == TokenType.LEFT_CURLY_BRACKET:
			result = self.parse_struct()
		elif self.token.type == TokenType.LEFT_ROUND_BRACKET:
			result = self.parse_stmts()
		elif self.token.type in [TokenType.VAR, TokenType.CON, TokenType.IF, TokenType.WHILE]:
			result = self.parse_stmt()
		else:
			error.highlight(self.token.position)
			print("Error: expected a number or identifier")
			exit()

		# call or index
		while self.token.type in [TokenType.LEFT_SQUARE_BRACKET, TokenType.LEFT_CURLY_BRACKET]:
			if self.token.type == TokenType.LEFT_SQUARE_BRACKET:
				result = IndexNode([self.advance()], [result])
				result.nodes.append(self.parse_expr())

				if self.token.type != TokenType.RIGHT_SQUARE_BRACKET:
					error.highlight(self.token.position)
					print("Error: expected `]` while parsing index")
					exit()

				result.tokens.append(self.advance())
			elif self.token.type == TokenType.LEFT_CURLY_BRACKET:
				result = CallNode([], [result, self.parse_struct()])

		return result



	# unary ::= ('+' | '-') unary
	#         | factor
	def parse_oper0(self):
		if self.token.type == TokenType.PLUS:
			return PosNode([self.advance()], self.parse_oper0())
		if self.token.type == TokenType.MINUS:
			return NegNode([self.advance()], self.parse_oper0())

		return self.parse_factor()

	# oper1 ::= oper1 ('*' | '/' | '%' | '<<' | '>>') unary
	#           unary
	def parse_oper1(self):
		result = self.parse_oper0()

		while self.token.type in [TokenType.ASTERISK, TokenType.SLASH, TokenType.PERCENT, TokenType.SHIFT_LEFT, TokenType.SHIFT_RIGHT]:
			if self.token.type == TokenType.ASTERISK:
				result = MulNode([self.advance()], [result, self.parse_oper0()])
			elif self.token.type == TokenType.SLASH:
				result = DivNode([self.advance()], [result, self.parse_oper0()])
			elif self.token.type == TokenType.PERCENT:
				result = ModNode([self.advance()], [result, self.parse_oper0()])
			elif self.token.type == TokenType.SHIFT_LEFT:
				result = ShlNode([self.advance()], [result, self.parse_oper0()])
			elif self.token.type == TokenType.SHIFT_RIGHT:
				result = ShrNode([self.advance()], [result, self.parse_oper0()])
			else:
				error.highlight(self.token.position)
				print("Error: internal error")
				exit()

		return result

	# oper2 ::= oper2 ('+' | '-') oper1
	#         | oper1
	def parse_oper2(self):
		result = self.parse_oper1()

		while self.token.type in [TokenType.PLUS, TokenType.MINUS]:
			if self.token.type == TokenType.PLUS:
				result = AddNode([self.advance()], [result, self.parse_oper1()])
			elif self.token.type == TokenType.MINUS:
				result = SubNode([self.advance()], [result, self.parse_oper1()])
			else:
				error.highlight(self.token.position)
				print("Error: internal error")
				exit()

		return result

	# oper3 ::= oper3 ('|' | '&' | '^') oper2
	#         | oper2
	def parse_oper3(self):
		result = self.parse_oper2()

		while self.token.type in [TokenType.BITWISE_OR, TokenType.BITWISE_AND, TokenType.BITWISE_XOR]:
			if self.token.type == TokenType.BITWISE_OR:
				result = BitOrNode([self.advance()], [result, self.parse_oper2()])
			elif self.token.type == TokenType.BITWISE_AND:
				result = BitAndNode([self.advance()], [result, self.parse_oper2()])
			elif self.token.type == TokenType.BITWISE_XOR:
				result = BitXorNode([self.advance()], [result, self.parse_oper2()])
			else:
				error.highlight(self.token.position)
				print("Error: internal error")
				exit()

		return result

	# oper4 ::= oper3 ('<' | '>' | '<=' | '>=') oper3
	def parse_oper4(self):
		result = self.parse_oper3()

		if self.token.type == TokenType.LESS_THAN:
			return LtNode([self.advance()], [result, self.parse_oper3()])
		if self.token.type == TokenType.GREATER_THAN:
			return GtNode([self.advance()], [result, self.parse_oper3()])
		if self.token.type == TokenType.LESS_THAN_OR_EQUAL:
			return LteNode([self.advance()], [result, self.parse_oper3()])
		if self.token.type == TokenType.GREATER_THAN_OR_EQUAL:
			return GteNode([self.advance()], [result, self.parse_oper3()])

		return result

	# oper5 ::= oper4 ('==' | '!=') oper4
	def parse_oper5(self):
		result = self.parse_oper4()

		if self.token.type == TokenType.EQUAL:
			return EqNode([self.advance()], [result, self.parse_oper4()])
		if self.token.type == TokenType.NOT_EQUAL:
			return NeqNode([self.advance()], [result, self.parse_oper4()])

		return result

	# expr ::= expr ('||' | '&&') oper5
	#        | oper5
	def parse_expr(self):
		result = self.parse_oper5()

		while self.token.type in [TokenType.OR, TokenType.AND]:
			if self.token.type == TokenType.OR:
				return OrNode([self.advance()], [result, self.parse_oper5()])
			elif self.token.type == TokenType.AND:
				return AndNode([self.advance()], [result, self.parse_oper5()])

		return result

	# array ::= '[' nls expr ((',' | \n nls) expr) nls ']'
	def parse_array(self):
		if self.token.type != TokenType.LEFT_SQUARE_BRACKET:
			error.highlight(self.token.position)
			print("Error: expected a `[` while parsing an array")
			exit()

		result = ArrayNode([self.advance()], [])

		self.skip_newlines()

		if self.token.type != TokenType.RIGHT_SQUARE_BRACKET:
			result.nodes.append(self.parse_expr())

		while self.token.type in [TokenType.COMMA, TokenType.NEWLINE]:
			self.advance()
			self.skip_newlines()

			if self.token.type == TokenType.RIGHT_SQUARE_BRACKET:
				break

			result.nodes.append(self.parse_expr())

		if self.token.type != TokenType.RIGHT_SQUARE_BRACKET:
			error.highlight(self.token.position)
			print("Error: expected a `]` while parsing an array")
			exit()

		result.nodes.append(self.advance())

		return result

	# struct ::= '{' nls expr ((',' | \n nls) expr) nls '}'
	def parse_struct(self):
		if self.token.type != TokenType.LEFT_CURLY_BRACKET:
			error.highlight(self.token.position)
			print("Error: expected a `{` while parsing a struct")
			exit()

		result = StructNode([self.advance()], [])

		self.skip_newlines()

		if self.token.type != TokenType.RIGHT_CURLY_BRACKET:
			result.nodes.append(self.parse_expr())

		while self.token.type in [TokenType.COMMA, TokenType.NEWLINE]:
			self.advance()
			self.skip_newlines()

			if self.token.type == TokenType.RIGHT_CURLY_BRACKET:
				break

			result.nodes.append(self.parse_expr())

		if self.token.type != TokenType.RIGHT_CURLY_BRACKET:
			error.highlight(self.token.position)
			print("Error: expected a `}` while parsing a struct")
			exit()

		result.tokens.append(self.advance())

		return result

	def parse_var(self):
		if self.token.type != TokenType.VAR:
			error.highlight(self.token.position)
			print("Error: expected a `var` while parsing a var statemnt")
			exit()

		result = VarNode([self.advance()], [])

		if self.token.type != TokenType.IDENTIFIER:
			error.highlight(self.token.position)
			print("Error: expected an identifier while parsing a var statemnt")
			exit()

		result.tokens.append(self.advance())

		if self.token.type != TokenType.SET:
			error.highlight(self.token.position)
			print("Error: expected a `=` while parsing a var statemnt")
			exit()

		result.tokens.append(self.advance())
		result.nodes.append(self.parse_expr())

		return result

	def parse_con(self):
		if self.token.type != TokenType.CON:
			error.highlight(self.token.position)
			print("Error: expected a `con` while parsing a con statemnt")
			exit()

		result = ConNode([self.advance()], [])

		if self.token.type != TokenType.IDENTIFIER:
			error.highlight(self.token.position)
			print("Error: expected an identifier while parsing a con statemnt")
			exit()

		result.tokens.append(self.advance())

		if self.token.type != TokenType.SET:
			error.highlight(self.token.position)
			print("Error: expected a `=` while parsing a con statemnt")
			exit()

		result.tokens.append(self.advance())
		result.nodes.append(self.parse_expr())

		return result

	def parse_if(self):
		if self.token.type != TokenType.IF:
			error.highlight(self.token.position)
			print("Error: expected a `if` while parsing an if statement")
			exit()

		result = IfNode([self.advance()], [self.parse_expr(), self.parse_stmts()])

		if self.token.type != TokenType.ELSE:
			return result

		result.tokens.append(self.advance())
		result.nodes.append(self.parse_stmts())

		return result

	def parse_while(self):
		if self.token.type != TokenType.WHILE:
			error.highlight(self.token.position)
			print("Error: expected a `while` while parsing an while statement")
			exit()

		return WhileNode([self.advance()], [self.parse_expr(), self.parse_stmts()])

	def parse_decl_func(self):
		if self.token.type != TokenType.FUNC:
			error.highlight(self.token.position)
			print("Error: expected a `func` while parsing a func decleration")
			exit()

		result = DeclFuncNode([self.advance()], [None, None, None])

		if self.token.type != TokenType.IDENTIFIER:
			error.highlight(self.token.position)
			print("Error: expected an identifier while parsing a func decleration")
			exit()

		result.tokens.append(self.advance())

		if self.token.type in [TokenType.TYPE_IDENTIFIER, TokenType.LEFT_CURLY_BRACKET]:
			result.nodes[0] = self.parse_type()

		if self.token.type == TokenType.TO:
			result.tokens.append(self.advance())

			if not self.token.type in [TokenType.TYPE_IDENTIFIER, TokenType.LEFT_CURLY_BRACKET]:
				error.highlight(self.token.position)
				print("Error: expected a type while parsing a func decleration")
				exit()

			result.nodes[1] = self.parse_type()

		result.nodes[2] = self.parse_stmts()

		return result


	def parse_set(self):
		result = self.parse_expr()

		if self.token.type == TokenType.SET:
			return SetNode([self.advance()], [result, self.parse_expr()])
		if self.token.type == TokenType.SET_PLUS:
			lexeme = self.advance()

			return SetNode([lexeme], [result, AddNode([lexeme], [result, self.parse_expr()])])
		if self.token.type == TokenType.SET_MINUS:
			lexeme = self.advance()

			return SetNode([lexeme], [result, SubNode([lexeme], [result, self.parse_expr()])])
		if self.token.type == TokenType.SET_ASTERISK:
			lexeme = self.advance()

			return SetNode([lexeme], [result, MulNode([lexeme], [result, self.parse_expr()])])
		if self.token.type == TokenType.SET_SLASH:
			lexeme = self.advance()

			return SetNode([lexeme], [result, DivNode([lexeme], [result, self.parse_expr()])])
		if self.token.type == TokenType.SET_PERCENT:
			lexeme = self.advance()

			return SetNode([lexeme], [result, ModNode([lexeme], [result, self.parse_expr()])])
		if self.token.type == TokenType.SET_SHIFT_LEFT:
			lexeme = self.advance()

			return SetNode([lexeme], [result, ShlNode([lexeme], [result, self.parse_expr()])])
		if self.token.type == TokenType.SET_SHIFT_RIGHT:
			lexeme = self.advance()

			return SetNode([lexeme], [result, ShrNode([lexeme], [result, self.parse_expr()])])
		if self.token.type == TokenType.SET_BITWISE_OR:
			lexeme = self.advance()

			return SetNode([lexeme], [result, BitOrNode([lexeme], [result, self.parse_expr()])])
		if self.token.type == TokenType.SET_BITWISE_AND:
			lexeme = self.advance()

			return SetNode([lexeme], [result, BitAndNode([lexeme], [result, self.parse_expr()])])
		if self.token.type == TokenType.SET_BITWISE_XOR:
			lexeme = self.advance()

			return SetNode([lexeme], [result, BitXorNode([lexeme], [result, self.parse_expr()])])

		return result

	def parse_stmt(self):
		self.skip_newlines()

		if self.token.type == TokenType.VAR:
			return self.parse_var()
		if self.token.type == TokenType.CON:
			return self.parse_con()
		if self.token.type == TokenType.IF:
			return self.parse_if()
		if self.token.type == TokenType.WHILE:
			return self.parse_while()
		if self.token.type == TokenType.FUNC:
			return self.parse_decl_func()

		return self.parse_set()

	def parse_stmts(self):
		if self.token.type != TokenType.LEFT_ROUND_BRACKET:
			return self.parse_stmt()

		result = StmtsNode([self.advance()], [])

		self.skip_newlines()

		if self.token.type != TokenType.RIGHT_ROUND_BRACKET:
			result.nodes.append(self.parse_stmt())

		while self.token.type == TokenType.NEWLINE:
			self.skip_newlines()

			if self.token.type == TokenType.RIGHT_ROUND_BRACKET:
				break

			result.nodes.append(self.parse_stmt())

		if self.token.type != TokenType.RIGHT_ROUND_BRACKET:
			error.highlight(self.token.position)
			print("Error: expected a `)` or a newline while parsing statements")
			exit()

		result.tokens.append(self.advance())

		return result

	def parse_prgrm(self):
		result = PrgrmNode([], [])

		self.skip_newlines()

		if self.token.type != TokenType.EOF:
			result.nodes.append(self.parse_stmt())

		while self.token.type == TokenType.NEWLINE:
			self.skip_newlines()

			if self.token.type == TokenType.EOF:
				break

			result.nodes.append(self.parse_stmt())

		if self.token.type != TokenType.EOF:
			error.highlight(self.token.position)
			print("Error: expected EOF while parsing program")
			exit()

		return result

	def parse(self):
		self.advance()

		return self.parse_decl_func()
