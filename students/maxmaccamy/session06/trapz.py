__author__ = 'Max'

STEPS = 11 # This equates to 10 different integration points.

def trapz(fun, a, b):
    """
    :param fun: The function to compute the area under defined as y = fun(x), for x between a and b.
    :type  fun: A funtion that takes a single parameter.

    :param a: Start point for the integration.
    :type  a: A numeric value.

    :param b: The end point for the integration.
    :type  b: A numeric value.

    :return: The computed area under the function (fun) from a to b. If any parameter is incorrect, this returns None.
    :type:   A numeric value.

    Compute the area under the curve defined by y = fun(x), for x between a and b.
    """

    if (b > a):
        values = []

        #Compute the step interval.
        #TODO: Check that a and b can both be converted to floats.
        stepValue = (b-a)/STEPS

        #Create a list of all of the points that need to be evaluated.
        stepPoints = [stepValue * i for i in range(1, STEPS)]

        #Return the sum of all of the steps.
        #Evaluate the first and last points since these are not doubled.
        result = fun(*stepPoints)

        #Now add in all of the other step points which are all doubled.
        for i in range(1, len(stepPoints) - 2):
            result += (2 * fun(*stepPoints))

        result *= (b-a)/(2*STEPS)
        return result
    else:
        print("Parameter b must be greater than a")
        return None

def getStepValues(a, b):
        #Create a list of all of the points that need to be evaluated.
        stepValue = (b-a)/STEPS

        return [stepValue * i for i in range(1, STEPS)]


if __name__ == '__main__':
    print(getStepValues(0, 10))
    getStepValues(10, 9)


