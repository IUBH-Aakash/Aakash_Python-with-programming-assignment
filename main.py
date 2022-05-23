import math
from function import FunctionManager
from regression import minimise_loss, find_classification
from lossfunction import squared_error
from plotting import plot_ideal_functions, plot_points_with_their_ideal_function
from utils import write_deviation_results_to_sqlite

# This constant is the accepted factor for the required criterion.
ACCEPTED_FACTOR = math.sqrt(2)

if __name__ == '__main__':
    # Path of the provided dataset in CSV format
    ideal_path = "IUBH_dataset/ideal.csv"
    train_path = "IUBH_dataset/train.csv"

    # Function_Manager will take the path of the CSV and it will fetch Function objects from the given dataset.
    # Function will store X and Y values of a function. Pandas will be used for this task
    # Four functions are stored in Train_function_manager
    # fifty functions are stored in Ideal_function_manager
    Ideal_function_manager = FunctionManager(path_of_csv=ideal_path)
    Train_function_manager = FunctionManager(path_of_csv=train_path)

    # .to_sql function will be used from Pandas library
    Train_function_manager.to_sql(file_name="training", suffix=" (training func)")
    Ideal_function_manager.to_sql(file_name="ideal", suffix=" (ideal func)")

    # Now further we will use the data to compute Ideal_Function with the train data.
    # Ideal-Function amongst others stores best fitting function, the train data and is able to compute the tolerance.
    # All we now need to do is iterate over all train_functions. Matching ideal functions are stored in a list.

    ideal_functions = []
    for train_function in Train_function_manager:
        # minimise_loss will compute the best fitting function from train function
        ideal_function = minimise_loss(training_function=train_function,
                                       list_of_candidate_functions=Ideal_function_manager.functions,
                                       loss_function=squared_error)
        ideal_function.tolerance_factor = ACCEPTED_FACTOR
        ideal_functions.append(ideal_function)

    # We will use classification method to do plotting
    plot_ideal_functions(ideal_functions, "train_and_ideal")

    # The role of FunctionManager is to provide all the necessary to load a CSV.
    # Rather than multiple Functions, it will contain a single "Function" at location [0], so that we can iterate over each point with the Function object.
    test_path = "IUBH_dataset/test.csv"
    test_function_manager = FunctionManager(path_of_csv=test_path)
    test_function = test_function_manager.functions[0]

    # 'points_with_ideal_functions' will be used to store the list of dictionaries, these dictionaries represent the classification result of each point.
    points_with_ideal_function = []
    for point in test_function:
        ideal_function, delta_y = find_classification(point=point, ideal_functions=ideal_functions)
        result = {"point": point, "classification": ideal_function, "delta_y": delta_y}
        points_with_ideal_function.append(result)

    # Now we will plot all the points with the corresponding classification function
    plot_points_with_their_ideal_function(points_with_ideal_function, "point_and_ideal")

    # Now dictionary object is used to write it to a sqlite. For this SQLAlchemy will be used with the Metadata.
    write_deviation_results_to_sqlite(points_with_ideal_function)
    print("Below Files will be created:")
    print("training.db: Contain training functions as sqlite database")
    print("ideal.db: Contain ideal functions as sqlite database")
    print("mapping.db: It will store the point test data in which the ideal function and its delta is computed")
    print("train_and_ideal.html: It will show the train data as scatter and the best fitting ideal function as curve")
    print("points_and_ideal.html: It will show those point with a matching ideal function the distance between them in a figure")

    print("Author: Aakash Dalal")
    print("Date: 22 May, 2022")
    print("Execution of script is complete")