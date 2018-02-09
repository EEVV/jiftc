from parser.lexer.token import Position

def highlight(position):
	line = position.source.splitlines()[position.line_start - 1]
	line_int = str(position.line_start)

	offset = position.col_start + len(line_int) + 2

	offset -= len(line)
	line = line.lstrip()
	offset += len(line)

	print("{} | {}".format(line_int, line))

	print(" " * offset, end = "")
	print("~" * (position.col_end - position.col_start - 1), end = "")
	print("^")
