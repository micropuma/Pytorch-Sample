import inspect

def functionDemo(a: int, b : float, c: str = "default") -> None:
    """
    This function demonstrates how to inspect function parameters.
    
    Parameters:
    a (int): An integer parameter.
    b (float): A float parameter.
    c (str): A string parameter with a default value.
    """
    print(f"a: {a}, b: {b}, c: {c}")

def inspectFunction(func):
    """
    Inspects the function and prints its signature and docstring.
    
    Parameters:
    func (function): The function to inspect.
    """
    signature = inspect.signature(func)

    for key, value in signature.parameters.items():
        print(f"Parameter: {key}, Type: {value.annotation}, Default: {value.default}")

if __name__ == "__main__":
    inspectFunction(functionDemo)