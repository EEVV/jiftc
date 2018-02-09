from enum import Enum, auto

class TokenType(Enum):
	NUMBER = auto()
	IDENTIFIER = auto()
	TYPE_IDENTIFIER = auto()

	# keywords
	FUNC = auto()
	STRUCT = auto()
	ENUM = auto()
	CON = auto()
	VAR = auto()
	IF = auto()
	ELSE = auto()
	WHILE = auto()

	PLUS = auto() # +
	MINUS = auto() # -
	ASTERISK = auto() # *
	SLASH = auto() # /
	PERCENT = auto() # %
	SHIFT_LEFT = auto() # <<
	SHIFT_RIGHT = auto() # >>
	BITWISE_AND = auto() # &
	BITWISE_OR = auto() # |
	BITWISE_XOR = auto() # ^

	SET = auto() # =
	SET_PLUS = auto() # +=
	SET_MINUS = auto() # -=
	SET_ASTERISK = auto() # *=
	SET_SLASH = auto() # /=
	SET_PERCENT = auto() # %=
	SET_SHIFT_LEFT = auto() # <<
	SET_SHIFT_RIGHT = auto() # >>
	SET_BITWISE_OR = auto() # |
	SET_BITWISE_AND = auto() # &
	SET_BITWISE_XOR = auto() # ^

	NOT = auto() # !
	LESS_THAN = auto() # <
	GREATER_THAN = auto() # >
	LESS_THAN_OR_EQUAL = auto() # <=
	GREATER_THAN_OR_EQUAL = auto() # >=
	EQUAL = auto() # ==
	NOT_EQUAL = auto() # !=

	OR = auto() # ||
	AND = auto() # &&

	LEFT_ROUND_BRACKET = auto() # (
	RIGHT_ROUND_BRACKET = auto() # )
	LEFT_SQUARE_BRACKET = auto() # [
	RIGHT_SQUARE_BRACKET = auto() # ]
	LEFT_CURLY_BRACKET = auto() # {
	RIGHT_CURLY_BRACKET = auto() # }

	COMMA = auto() # ,
	DOT = auto() # .
	TO = auto() # ->
	COLON = auto() # :

	NEWLINE = auto() # \n
	EOF = auto()

class Position:
	def __init__(self, source, pos_start, pos_end, col_start, col_end, line_start, line_end):
		self.source = source

		self.pos_start = pos_start
		self.pos_end = pos_end

		self.col_start = col_start
		self.col_end = col_end

		self.line_start = line_start
		self.line_end = line_end

class Token:
	def __init__(self, value, type, position):
		self.value = value
		self.type = type
		self.position = position

	def __str__(self):
		return "{} {}".format(str(self.type), self.value)
