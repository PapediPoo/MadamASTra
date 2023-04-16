import subprocess

class Z3Driver():
    __process = None
    __output_buffer = []

    def __init__(self) -> None:
        self.__process = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def kill(self) -> None:
        pass

    def writeln(self, command: str) -> None:
        output = self.__process.communicate(command.encode())
        for ln in output:
            print(ln.decode())

    def readln(self) -> str:
        pass
