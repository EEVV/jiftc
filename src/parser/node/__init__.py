
class Node:
	def __init__(self, tokens, nodes = None):
		self.tokens = tokens
		self.nodes = nodes

class NumNode(Node):
	# self.tokens[0] -> token

	def __init__(self, tokens):
		super().__init__(tokens)

	def __str__(self):
		return "({})".format(self.tokens[0].value)

	def __repr__(self):
		return "NumNode(\n{})".format(repr(tokens))

class IdenNode(Node):
	# self.token[0] -> token

	def __init__(self, tokens):
		super().__init__(tokens)

	def __str__(self):
		return "({})".format(self.tokens[0].value)

class ArrayNode(Node):
	# self.tokens[0] -> first '['
	# self.tokens[-1] -> last ']'

	# self.nodes[n] -> expr

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		result = "(array"

		for node in self.nodes:
			result += " " + str(node)

		return result + ")"

class StructNode(Node):
	# self.tokens[0] -> first '{'
	# self.tokens[-1] -> last '}'

	# self.nodes[n] -> expr

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		result = "(struct"

		for node in self.nodes:
			result += " " + str(node)

		return result + ")"

# operators

class PosNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

		self.nodes = nodes

	def __str__(self):
		return "(+ {})".format(str(self.node))

class NegNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(- {})".format(str(self.node))

class AddNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(+ {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class SubNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(- {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class MulNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(* {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class DivNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(/ {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class ModNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(% {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class ShlNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(<< {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class ShrNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(>> {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class BitOrNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(| {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class BitAndNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(& {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class BitXorNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(^ {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class LtNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(< {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class GtNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(> {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class LteNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(<= {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class GteNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(>= {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class EqNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(== {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class NeqNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(!= {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class OrNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(|| {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class AndNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(&& {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class IndexNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(index {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

# statements

class PrgrmNode(Node):
	# self.nodes[n] -> stmt | func decl | struct decl | enum decl

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		result = "(prgrm"

		for node in self.nodes:
			result += " " + str(node)

		return result + ")"

class StmtsNode(Node):
	# self.tokens[0] -> first '('
	# self.token[-1] -> last ')'

	# self.nodes[n] -> stmt | func decl | struct decl | enum decl

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		result = "(stmts"

		for node in self.nodes:
			result += " " + str(node)

		return result + ")"

class VarNode(Node):
	# self.nodes[0] -> right operand

	# self.tokens[0].value -> `var`
	# self.tokens[1] -> left operand (identifier)
	# self.tokens[2].value -> `=`

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(var ({}) {})".format(self.tokens[1].value, str(self.nodes[0]))

class ConNode(Node):
	# self.nodes[0] -> right operand

	# self.tokens[0].value -> `con`
	# self.tokens[1] -> left operand (identifier)
	# self.tokens[2].value -> `=`

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(con ({}) {})".format(self.tokens[1].value, str(self.nodes[0]))

class SetNode(Node):
	# self.nodes[0] -> left operand
	# self.nodes[1] -> right operand

	# self.tokens[0].value -> `=`

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(= {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

class IfNode(Node):
	# self.nodes[0] -> condition
	# self.nodes[1] -> true
	# self.nodes[2] -> false?

	# self.tokens[0].value -> `if`
	# self.token[1].value -> `else`?

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		result = "(if"

		for node in self.nodes:
			result += " " + str(node)

		return result + ")"

class WhileNode(Node):
	# self.nodes[0] -> condition
	# self.nodes[1] -> stmts

	# self.tokens[0].value -> `while`

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		result = "(while"

		for node in self.nodes:
			result += " " + str(node)

		return result + ")"

class CallNode(Node):
	# self.nodes[0] -> callee
	# self.nodes[1] -> struct

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		return "(call {} {})".format(str(self.nodes[0]), str(self.nodes[1]))

# declared

class DeclFuncNode(Node):
	# self.node[0] -> input
	# self.node[1] -> output
	# self.node[2] -> body

	# self.tokens[0].value -> `func`
	# self.tokens[1].value -> name
	# self.tokens[2].value -> `->`

	def __init__(self, tokens, nodes):
		super().__init__(tokens, nodes)

	def __str__(self):
		result = "(declfunc (" + self.tokens[1].value + ")"

		if self.nodes[0] != None:
			result += " (in " + str(self.nodes[0]) + ")"

		if self.nodes[1] != None:
			result += " (out " + str(self.nodes[1]) + ")"

		if self.nodes[2] != None:
			result += " " + str(self.nodes[2])

		return result + ")"



# type nodes

class Field:
	def __init__(self, name, type):
		self.name = name
		self.type = type

	def __str__(self):
		result = "(field"
		if self.name != None:
			result += " (" + self.name.value + ")"

		if self.type != None:
			result += " " + str(self.type)

		return result + ")"

class TypeNode:
	def __init__(self, tokens):
		self.tokens = tokens

class IdenTypeNode(TypeNode):
	def __init__(self, tokens):
		super().__init__(tokens)

	def __str__(self):
		return "(identype ({}))".format(self.tokens[0].value)

class ArrayTypeNode(TypeNode):
	def __init__(self, tokens, node):
		super().__init__(tokens)

		self.node = node

	def __str__(self):
		return "(arraytype {})".format(str(self.node))

class StructTypeNode(TypeNode):
	def __init__(self, tokens, fields):
		super().__init__(tokens)

		self.fields = fields

	def __str__(self):
		result = "(structtype"

		for field in self.fields:
			result += " " + str(field)

		return result + ")"
