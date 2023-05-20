import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

df = pd.read_csv("rc.csv")
soc = df.iloc[:, 0].values
r0 = df.iloc[:, 1].values
r1 = df.iloc[:, 2].values
c1 = df.iloc[:, 3].values
xx = np.linspace(soc.min(), soc.max(), 100)

for y in [r0, r1, c1]:
    f = interp1d(soc, y, kind="cubic")
    yy = f(xx)
    plt.plot(soc, y, "o")
    plt.plot(xx, yy)
    plt.show()
