#STARNDARD LAGRANGE FORMULA (BY CEDRIC)
def lagrange_interpolation(x_points, y_points, x):
  
    #Number of X Points
    n = len(x_points)
    total = 0.0

    for i in range(n):
        # Formula L_i(x) BIG π x-xi/xi-xj
        Li = 1.0
        for j in range(n):
            if i != j:
                Li *= (x - x_points[j]) / (x_points[i] - x_points[j])

        #Summation of Y[i] and Lagrange Big Pi Multiplication
        total += y_points[i] * Li #My Change

    return total

def main():
    #  Ask how many data points
    while True:
        try:
            #Ask the user how many points they want to input (2-5)
            n = int(input("How many data points (2-5)? "))
            if 2 <= n <= 5:
                break
            #Invalid Input Handling
            else:
                print("Please enter an integer between 2 and 5.")
        except ValueError:
            print("Please enter a valid integer.")

    # Constant Array [1,2,3,4,5] for X Points
    x_points = list(range(1, n + 1))  # [1,2] or [1,2,3] or [1,2,3,4] or [1,2,3,4,5]n (My change)

    #Empty Y Points Array to be filled by user input
    y_points = []

    #  Ask for Y1..Yn
    print("\nEnter the y-values:")
    for i in range(n):
        while True:
            #Valid Input
            try:
                y_val = float(input(f"Y{i}: "))
                y_points.append(y_val)
                break
            #Invalid Input
            except ValueError:
                print("Please enter a valid number.")

    # Temporary Commented Out Single Input Test Case
    """
    #  Ask for the x where P(x) is needed
    while True:
        try:
            x = float(input("\nEnter the value of x where you want to evaluate P(x): "))
            break
        except ValueError:
            print("Please enter a valid number.")

    #  Compute and print result
    result = lagrange_interpolation(x_points, y_points, x)
    print(f"\nThe estimated value P({x}) is: {result}")
    """
    
    #Using Sequential Indices (1,2,3,4,5) to Try out Test Cases (3-5 Data Points Advance). This works better somehow.
    #This is my change
    for j in range (5):
        print(f"\n--- Test Case: Estimating P({5+(j+1)}) ---")
        result = lagrange_interpolation(x_points, y_points, 5+(j+1))
        print(f"\nThe estimated value P({5+(j+1)}) is: {result}")

if __name__ == "__main__":
    main()
    