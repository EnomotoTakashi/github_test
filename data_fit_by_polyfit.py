import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
for i in range(1, 10):
    po = np.polyfit(df.iloc[:, 0] / 100, df.iloc[:, 1], i)
    xx = np.linspace(-0.05, 1.05, 200)
    yy = np.polyval(po, xx)
    plt.plot(df.iloc[:, 0] / 100, df.iloc[:, 1], "o")
    plt.plot(xx, yy)
    plt.show()

degree = 6
po = np.polyfit(df.iloc[:, 0] / 100, df.iloc[:, 1], degree)
with open("degree.csv", "w") as fout:
    for p in po:
        print(f"{p:.4e}", file=fout)
