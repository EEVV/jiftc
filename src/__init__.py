from parser import Parser


def main():
	source_file = open("../examples/mult.jift", "r")
	source = source_file.read()
	source_file.close()

	parser = Parser(source)

	for token in parser.lexer.get_tokens():
		print(token)

	parser.reset()

	print()

	print(parser.parse())

if __name__ == "__main__":
	main()
