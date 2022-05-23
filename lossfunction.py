def squared_error(first_function, second_function):
    """
    Calculation of squared error to another function
    :parameter other_function:
    :return: the squared error
    """
    distances = second_function - first_function
    distances["y"] = distances["y"] ** 2
    total_deviation = sum(distances["y"])
    return total_deviation

