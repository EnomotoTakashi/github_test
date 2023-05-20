import numpy as np
import matplotlib.pyplot as plt

def calculate_ocv(soc):
    """
    Calculate the open circuit voltage (ocv) based on state of charge (soc) and given coefficients (c).
    
    Parameters:
    soc (numpy.ndarray or float): The state of charge. This can be a single float value or a numpy array.
    c (numpy.ndarray): The array of coefficients for the polynomial. 

    Returns:
    numpy.ndarray or float: The open circuit voltage (ocv). This will be a numpy array if soc is a numpy array, 
    otherwise a single float value.
    """
    c = np.array([-1.2918e+00, 9.6896e+00, -2.1023e+01, 1.9749e+01, -8.0028e+00, 1.6362e+00, 3.4722e+00])
    return sum(coefficient * soc ** power for power, coefficient in enumerate(c[::-1]))

# Coefficients for the polynomial
# c = np.array([-1.2918e+00, 9.6896e+00, -2.1023e+01, 1.9749e+01, -8.0028e+00, 1.6362e+00, 3.4722e+00])

# Create an array of soc values
soc_values = np.linspace(-0.1, 1.1, 200)

# Calculate ocv values for the array of soc values
ocv_values = calculate_ocv(soc_values)

# Uncomment below lines to plot soc_values vs ocv_values
# plt.plot(soc_values, ocv_values)
# plt.show()

# Calculate ocv for a single soc value
soc = 0.7
ocv = calculate_ocv(soc)
print(ocv)




# import numpy as np
# import matplotlib.pyplot as plt

# c = np.array([-1.2918e+00,
#                 9.6896e+00,
#                 -2.1023e+01,
#                 1.9749e+01,
#                 -8.0028e+00,
#                 1.6362e+00,
#                 3.4722e+00])

# soc = np.linspace(-0.1, 1.1, 200)
# ocv = c[0] * soc ** 6 + \
#         c[1] * soc ** 5 + \
#         c[2] * soc ** 4 + \
#         c[3] * soc ** 3 + \
#         c[4] * soc ** 2 + \
#         c[5] * soc ** 1 + \
#         c[6] * soc ** 0
# # plt.plot(soc, ocv)
# # plt.show()

# soc = 0.7
# ocv = c[0] * soc ** 6 + \
#         c[1] * soc ** 5 + \
#         c[2] * soc ** 4 + \
#         c[3] * soc ** 3 + \
#         c[4] * soc ** 2 + \
#         c[5] * soc ** 1 + \
#         c[6] * soc ** 0
# print(ocv)
