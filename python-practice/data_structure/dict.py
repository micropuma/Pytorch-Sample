def helloWorld():
    print("Hello World")

def printB(b: int):
    print(b)


function = {
    "hello": helloWorld,
    "hellob": printB,
}

if __name__ == "__main__":
    function["hello"]()
    function["hellob"](5)
