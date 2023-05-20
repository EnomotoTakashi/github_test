# https://okumuralab.org/~okumura/python/plot2data.htmlより

import numpy as np
import matplotlib.pyplot as plt

fig_name = "fig2.png"
known_axis_value = (0, 60, 2.6, 4) # 既知の座標値

img = plt.imread(fig_name)
y_size, x_size, _ = img.shape
x_dim = 12
y_dim = x_dim * y_size / x_size
plt.figure(figsize=(x_dim, y_dim))
plt.imshow(img)

x_min, x_max, y_min, y_max = known_axis_value
fig_val = np.zeros(4)

# x_min, x_max, y_min, y_maxの順にクリック
ps = plt.ginput(4, timeout=0)
fig_val[0] = ps[0][0]
fig_val[1] = ps[1][0]
fig_val[2] = ps[2][1]
fig_val[3] = ps[3][1]
print(f"x min = ({x_min}, {fig_val[0]})")
print(f"x max = ({x_max}, {fig_val[1]})")
print(f"y min = ({y_min}, {fig_val[2]})")
print(f"y max = ({y_max}, {fig_val[3]})")

# プロット点を順に1回ずつクリック
# 右クリック（Ctrl-クリック）で一つ前を削除
# 中クリック（Alt-クリック）で終了
p = plt.ginput(-1, timeout=0)

def convert(t, t1, t2, u1, u2):
    return (u2 - u1) * (t - t1) / (t2 - t1) + u1

with open("data.csv", "w") as fout:
    print("x,y", file=fout)
    for x, y in p:
        x = convert(x, fig_val[0], fig_val[1], x_min, x_max)
        y = convert(y, fig_val[2], fig_val[3], y_min, y_max)
        print(f"{x:.3f},{y:.3f}", file=fout)
plt.close()
