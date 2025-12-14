# STANDARD LAGRANGE FORMULA (BY CEDRIC)
def lagrange_interpolation(x_points, y_points, x):
    n = len(x_points)
    total = 0.0
 #Summation of Y[i] and Lagrange Big Pi Multiplication
    for i in range(n):
        Li = 1.0
        for j in range(n):
            if i != j:
                Li *= (x - x_points[j]) / (x_points[i] - x_points[j])
        total += y_points[i] * Li

    return total
#formula for relative error
TRUE_VALUE = 5.0  # fixed true value
def relative_error(true_value, approx_value):
    # |true - approx| / |true|
    return abs(true_value - approx_value) / abs(approx_value)

def main():
    # Ask how many data points
    while True:
        try:
            n = int(input("How many data points (2-5)? "))
            if 2 <= n <= 5:
                break
            else:
                print("Please enter an integer between 2 and 5.")
        except ValueError:
            print("Please enter a valid integer.")

    # X points: 1,2,...,n
    x_points = list(range(1, n + 1))

    # Y points from user
    y_points = []
    print("\nEnter the y-values:")
    for i in range(n):
        while True:
            try:
                y_val = float(input(f"Y{i+1}: "))
                y_points.append(y_val)
                break
            except ValueError:
                print("Please enter a valid number.")
    #  Calculate Relative Error and Accuracy of Each Shot

    for k in range(n):
        x_test = k + 1  # 1..n
        print(f"\n--- Test Case: Estimating P({x_test}) ---")
        approx = lagrange_interpolation(x_points, y_points, x_test)
        print(f"Estimated value P({x_test}) = {approx}")

        rel_err = relative_error(TRUE_VALUE, approx)
        print(f"Relative error at x = {x_test}: {round(rel_err,3)}")

        accuracy = (1 - rel_err) * 100
        print(f"Accuracy at x = {x_test}: {round(accuracy,3)}%")

    # Test cases for x = 6,7,8,9,10
    for j in range(5):
        x_test = 5 + (j + 1)  # 6..10
        print(f"\n--- Test Case: Estimating P({x_test}) ---")
        approx = lagrange_interpolation(x_points, y_points, x_test)
        print(f"Estimated value P({x_test}) = {round(approx,3)}")
        if (approx > 5):
            approx = 10 - approx
            print(f"Manipulated value is: {round(approx,3)}")
            continue

        rel_err = relative_error(TRUE_VALUE, approx)
        print(f"Relative error at x = {x_test}: {rel_err}")

if __name__ == "__main__":
    main()
#me cedric is not goat anymore huhuhu :(
