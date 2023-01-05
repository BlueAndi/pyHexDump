"""Utilities
"""

def get_only_operators(list_of_methods):
    """Get only operators back from a list of method names.

    Args:
        list_of_methods (list): List of method names

    Returns:
        list: List of operators
    """
    result = []

    for element in list_of_methods:
        if (element.startswith("__") is True) and (element.endswith("__")):
            result.append(element)

    return result

def print_operators(obj):
    """Print the operators of a object to the CLI.

    Args:
        obj (obj): The object which to print the operators.
    """
    print(f"{obj} operators:")
    operators = get_only_operators(dir(obj))
    for element in operators:
        print(f"* {element}")
    print("\n")

if __name__ == "__main__":
    print_operators(int)
    print_operators(float)
    print_operators(list)
