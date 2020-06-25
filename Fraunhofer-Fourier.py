import cmath
import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib.colors as clr
import readimgcolor

fname = "test1.png"
wavelength = float(input("golflengte: "))
outname = input("naam output: ")
pixelsize = (0.05e-3, 0.05e-3)
intensity = 1
emitters = np.array([0, 0, 0, 0])
observplanez = 3.05e0
observplanesize = (5e-1, 5e-1)
observres = (1000, 1000)
cmap = clr.LinearSegmentedColormap.from_list(
    "blackgreen", ["#000000", "#00FF00"], N=512,
)
k = 2 * np.pi / wavelength
c = 299792458


def Umake(x, y, z, img):
    ftrans = np.zeros_like(x, dtype="complex128")
    print(np.shape(x), np.shape(y), np.shape(ftrans))
    for n, line in enumerate(img):
        if line[2] != 0:
            ax = line[1] * pixelsize[0]
            ay = line[0] * pixelsize[1]
            ftrans += (
                line[2]
                * intensity
                * pixelsize[0]
                * pixelsize[1]
                * np.exp(2j * np.pi * ax * x / (wavelength * z))
                * np.exp(2j * np.pi * ay * y / (wavelength * z))
                * np.sinc(pixelsize[0] * x / (wavelength * z))
                * np.sinc(pixelsize[1] * y / (wavelength * z))
            )
        if n % 50 == 0:
            print(n)
    return ftrans


bw = readimgcolor.bwplaatje(fname)


# use the emitters to calculate the interference on every point of the target
xs = np.linspace(-observplanesize[0] / 2, observplanesize[0] / 2, observres[0])
ys = np.linspace(-observplanesize[1] / 2, observplanesize[1] / 2, observres[1])
xx, yy = np.meshgrid(xs, ys)
print(f"meshgrid of size {observres[0]} by {observres[1]} has been made")
s = Umake(xx, yy, observplanez, bw)
# I = np.real_if_close(s * np.conjugate(s))
fig, ax = plt.subplots(figsize=(16, 9), tight_layout=True)
I = np.abs(s)
ax.pcolormesh(xx, yy, I, cmap=cmap)
fig.savefig(fname=outname, dpi=1000)
plt.show()
