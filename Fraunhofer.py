import cmath
import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib as mpl
import readimgcolor

fname = "test1.png"
wavelength = 500e-9
pixelsize = (0.05e-3, 0.05e-3)
pixelamt = (1, 1)
intensity = 1
emitters = np.array([0, 0, 0, 0])
observplanez = 3.05e0
observplanesize = (5e-1, 5e-1)
observres = (400, 400)
cmap = mpl.cm.cool

def U

bw = readimgcolor.bwplaatje(fname)
# create all emitter instances needed
for line in bw:
    if line[2] != 0:
        ys = np.linspace(
            (line[0] - 0.5) * pixelsize[0], (line[0] + 0.5) * pixelsize[0], pixelamt[0]
        )
        xs = np.linspace(
            (line[1] - 0.5) * pixelsize[1], (line[1] + 0.5) * pixelsize[1], pixelamt[1]
        )
        xx, yy = np.meshgrid(xs, ys)
        x = np.ravel(xx)
        y = np.ravel(yy)
        emitters = np.vstack((emitters, np.hstack((x, y, line[2] * intensity, 0))))
print(emitters)
print(f"{len(emitters)} emitters have been created")


# use the emitters to calculate the interference on every point of the target
xs = np.linspace(-observplanesize[0] / 2, observplanesize[0] / 2, observres[0])
ys = np.linspace(-observplanesize[1] / 2, observplanesize[1] / 2, observres[1])
xx, yy = np.meshgrid(xs, ys)
print(f"meshgrid of size {observres[0]} by {observres[1]} has been made")
s = sum()
I = np.abs(s)
plt.pcolormesh(xx, yy, I, cmap=cmap)
plt.colorbar()
plt.show()
