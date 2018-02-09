from parser.lexer.token import TokenType, Position, Token

import parser.lexer.error

class Lexer:
	def __init__(self, source):
		self.source = source

		self.reset()

	def reset(self):
		self.character = self.source[0]
		self.pos = 0
		self.line = 1
		self.col = 1
		self.position = Position(self.source, 0, None, 1, None, 1, None)

	def advance(self):
		self.pos += 1

		self.col += 1

		if self.character == '\n':
			self.line += 1
			self.col = 1

		if self.pos >= len(self.source):
			self.character = None
		else:
			self.character = self.source[self.pos]

	def gen_position(self):
		self.position.pos_end = self.pos
		self.position.col_end = self.col
		self.position.line_end = self.line

	def gen_token(self, value, type):
		self.gen_position()

		return Token(value, type, self.position)

	def get_number(self):
		result = self.character

		self.advance()

		while self.character != None and self.character.isdigit():
			result += self.character

			self.advance()

		if self.character == '.':
			result += '.'

			self.advance()

			if self.character == None or not self.character.isdigit():
				self.gen_position()
				error.highlight(self.position)
				print("Error: expected digit after the dot")

				exit()

			while self.character != None and self.character.isdigit():
				result += self.character

				self.advance()

		return result

	def get_identifier(self):
		result = self.character

		self.advance()

		while self.character != None and (self.character.isalpha() or self.character.isdigit()):
			result += self.character

			self.advance()

		return result

	def get_type_identifier(self):
		result = self.character

		self.advance()

		while self.character != None and (self.character.isalpha() or self.character.isdigit()):
			result += self.character

			self.advance()

		return result

	def get_token(self):
		if self.character == None:
			return self.gen_token('', TokenType.EOF)

		while self.character in [' ', '\t']:
			self.advance()

		if self.character == '#':
			while self.character != '\n':
				self.advance()

		self.position = Position(self.source, self.pos, None, self.col, None, self.line, None)

		if self.character.isdigit():
			return self.gen_token(self.get_number(), TokenType.NUMBER)

		if self.character.isalpha() and self.character.islower():
			identifier = self.get_identifier()

			return self.gen_token(identifier, {
				"func": TokenType.FUNC,
				"struct": TokenType.STRUCT,
				"enum": TokenType.ENUM,
				"con": TokenType.CON,
				"var": TokenType.VAR,
				"if": TokenType.IF,
				"else": TokenType.ELSE,
				"while": TokenType.WHILE,
				# types
				"u8": TokenType.TYPE_IDENTIFIER,
				"u16": TokenType.TYPE_IDENTIFIER,
				"u32": TokenType.TYPE_IDENTIFIER,
				"u64": TokenType.TYPE_IDENTIFIER,
				"i8": TokenType.TYPE_IDENTIFIER,
				"i16": TokenType.TYPE_IDENTIFIER,
				"i32": TokenType.TYPE_IDENTIFIER,
				"i64": TokenType.TYPE_IDENTIFIER,
				"f16": TokenType.TYPE_IDENTIFIER,
				"f32": TokenType.TYPE_IDENTIFIER,
				"f64": TokenType.TYPE_IDENTIFIER,
				"f80": TokenType.TYPE_IDENTIFIER,
				"uint": TokenType.TYPE_IDENTIFIER,
				"int": TokenType.TYPE_IDENTIFIER
			}.get(identifier, TokenType.IDENTIFIER))

		if self.character.isalpha() and self.character.isupper():
			return self.gen_token(self.get_identifier(), TokenType.TYPE_IDENTIFIER)

		if self.character == '+':
			self.advance()

			if self.character == '=':
				self.advance()

				return self.gen_token('+=', TokenType.SET_PLUS)

			return self.gen_token('+', TokenType.PLUS)
		if self.character == '-':
			self.advance()

			if self.character == '=':
				self.advance()

				return self.gen_token('-=', TokenType.SET_MINUS)
			if self.character == '>':
				self.advance()

				return self.gen_token('->', TokenType.TO)

			return self.gen_token('-', TokenType.MINUS)
		if self.character == '*':
			self.advance()

			if self.character == '=':
				self.advance()

				return self.gen_token('*=', TokenType.SET_ASTERISK)

			return self.gen_token('*', TokenType.ASTERISK)
		if self.character == '/':
			self.advance()

			if self.character == '=':
				self.advance()

				return self.gen_token('/=', TokenType.SET_SLASH)

			return self.gen_token('/', TokenType.SLASH)
		if self.character == '%':
			self.advance()

			if self.character == '=':
				self.advance()

				return self.gen_token('%=', TokenType.SET_PERCENT)

			return self.gen_token('%', TokenType.PERCENT)
		if self.character == '|':
			self.advance()

			if self.character == '=':
				self.advance()

				return self.gen_token('|=', TokenType.SET_BITWISE_OR)
			if self.character == '|':
				self.advance()

				return self.gen_token('||', TokenType.OR)

			return self.gen_token('|', TokenType.BITWISE_OR)
		if self.character == '&':
			self.advance()

			if self.character == '=':
				self.advance()

				return self.gen_token('&=', TokenType.SET_BITWISE_AND)
			if self.character == '&':
				self.advance()

				return self.gen_token('&&', TokenType.AND)

			return self.gen_token('&', TokenType.BITWISE_AND)
		if self.character == '^':
			self.advance()

			if self.character == '=':
				self.advance()

				return self.gen_token('^=', TokenType.SET_BITWISE_XOR)

			return self.gen_token('^', TokenType.BITWISE_XOR)

		if self.character == '=':
			self.advance()

			if self.character == '=':
				self.advance()

				return self.gen_token('==', TokenType.EQUAL)

			return self.gen_token('=', TokenType.SET)

		if self.character == '!':
			self.advance()

			if self.character == '=':
				self.advance()

				return self.gen_token('!=', TokenType.NOT_EQUAL)

			return self.gen_token('!', TokenType.NOT)

		if self.character == '<':
			self.advance()

			if self.character == '<':
				self.advance()

				if self.character == '=':
					self.advance()

					return self.gen_token('<<=', TokenType.SET_SHIFT_LEFT)

				return self.gen_token('<<', TokenType.SHIFT_LEFT)
			if self.character == '=':
				self.advance()

				return self.gen_token('<=', TokenType.LESS_THAN_OR_EQUAL)

			return self.gen_token('<', TokenType.LESS_THAN)
		if self.character == '>':
			self.advance()

			if self.character ==  '>':
				self.advance()

				if self.character == '=':
					self.advance()

					return self.gen_token('>>=', TokenType.SET_SHIFT_RIGHT)

				return self.gen_token('>>', TokenType.SHIFT_RIGHT)
			if self.character == '=':
				self.advance()

				return self.gen_token('>=', TokenType.GREATER_THAN_OR_EQUAL)

			return self.gen_token('>', TokenType.GREATER_THAN)

		if self.character == '(':
			self.advance()

			return self.gen_token('(', TokenType.LEFT_ROUND_BRACKET)
		if self.character == ')':
			self.advance()

			return self.gen_token(')', TokenType.RIGHT_ROUND_BRACKET)
		if self.character == '[':
			self.advance()

			return self.gen_token('[', TokenType.LEFT_SQUARE_BRACKET)
		if self.character == ']':
			self.advance()

			return self.gen_token(']', TokenType.RIGHT_SQUARE_BRACKET)
		if self.character == '{':
			self.advance()

			return self.gen_token('{', TokenType.LEFT_CURLY_BRACKET)
		if self.character == '}':
			self.advance()

			return self.gen_token('}', TokenType.RIGHT_CURLY_BRACKET)

		if self.character == ',':
			self.advance()

			return self.gen_token(',', TokenType.COMMA)
		if self.character == '.':
			self.advance()

			return self.gen_token('.', TokenType.DOT)
		if self.character == ':':
			self.advance()

			return self.gen_token(':', TokenType.COMMA)

		if self.character == '\n':
			self.advance()

			return self.gen_token('', TokenType.NEWLINE)

		self.position.pos_end = self.pos
		self.position.col_end = self.col
		self.position.line_end = self.line

		error.highlight(self.position)
		print("Error: invalid character")

		exit()

	def get_tokens(self):
		result = [self.get_token()]

		while result[-1].type != TokenType.EOF:
			result.append(self.get_token())

		return result
