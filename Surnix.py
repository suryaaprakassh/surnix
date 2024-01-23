import sys


class Surnix:
    had_error = False

    @staticmethod
    def __run(source, reset=False):
        from Scanner import Scanner
        scanner = Scanner(source)
        if (reset):
            scanner.reset()
        tokens = scanner.scan_tokens()
        print("tokens---->", tokens)

    @staticmethod
    def run_file(fileName):
        try:
            with open(fileName, 'r') as f:
                for line in f:
                    Surnix.__run(line)
                    if (Surnix.had_error):
                        sys.exit(65)
        except FileNotFoundError:
            print(f"File {fileName} not found")

    @staticmethod
    def run_prompt():
        while True:
            line = input('> ')
            if not line or line == "":
                had_error = True
                break
            Surnix.__run(line, True)
            had_error = False

    @staticmethod
    def error_token(token, message: str):
        from TokenType import TokenType
        if token.type == TokenType.EOF:
            Surnix.report(token.line, " at end", message)
        else:
            Surnix.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def error(line: int, message: str):
        Surnix.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        Surnix.had_error = True
