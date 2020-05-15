import cmath
import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib as mpl
import readimgcolor

fname = "test1.png"
wavelength = 500e-9
pixelsize = (0.05e-3, 0.05e-2)
pixelamt = (2, 20)
intensity = 1
emitters = []
observplanez = 3.05e0
observplanesize = (5e-1, 5e-1)
observres = (1000, 1000)
cmap = mpl.cm.cool


def EV(x, y, wl, intensity, z=0):
    return Emitter(x, y, wl, intensity, z)


def dist(x, y, z):
    return np.sqrt(x ** 2 + y ** 2 + z ** 2)


rekt = np.vectorize(cmath.rect)

# def A(a, k):
#     return lambda t: cmath.rect(a, k * np.c * t)


# def X(k, x, y, z):
#     return lambda xa, ya: cmath.rect(1, -k / z * (xa * x + ya * y))


# def U(a, k, x, y, z):
#     return lambda xa, ya, t: A(a, k)(t) * X(k, x, y, z)(xa, ya)


class Emitter:
    def __init__(self, x: float, y: float, wl: float, intensity: float, z: float = 0):
        self.x = x
        self.y = y
        self.z = z
        self.wl = wl
        self.int = intensity

    def wldist(self, x, y, z):
        return rekt(
            self.int, 2 * np.pi * dist(self.x - x, self.y - y, self.z - z) / self.wl
        )


bw = readimgcolor.bwplaatje(fname)
EVV = np.vectorize(EV)
# create all emitter instances needed
for line in bw:
    if line[2] != 0:
        xs = np.linspace(
            (line[0] - 0.5) * pixelsize[0], (line[0] + 0.5) * pixelsize[0], pixelamt[0]
        )
        ys = np.linspace(
            (line[1] - 0.5) * pixelsize[1], (line[1] + 0.5) * pixelsize[1], pixelamt[1]
        )
        xx, yy = np.meshgrid(xs, ys)
        emitters.extend(EVV(xx, yy, wavelength, line[2] * intensity).ravel())


# use the emitters to calculate the interference on every point of the target
xs = np.linspace(-observplanesize[0] / 2, observplanesize[0] / 2, observres[0])
ys = np.linspace(-observplanesize[1] / 2, observplanesize[1] / 2, observres[1])
xx, yy = np.meshgrid(xs, ys)
s = sum([o.wldist(xx, yy, observplanez) for o in emitters])
I = np.abs(s)
plt.pcolormesh(xx, yy, I, cmap=cmap)
plt.colorbar()
plt.show()
