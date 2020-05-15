import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
import readimg
import math
import matplotlib as mpl

fname = "test.png"
wavelength = 500e-9
pixelsize = 0.125e-3
pixelamt = (10, 10)
intensity = 1
emitters = []
observplanez = 1e0
observplanesize = (1, 1)
observres = (1000, 1000)
cmap = mpl.cm.cool


def pyta(x, y, z):
    return np.sqrt(x ** 2 + y ** 2 + z ** 2)


def EV(x, y, wl, intensity, z=0):
    return Emitter(x, y, wl, intensity, z)


class Emitter:
    def __init__(self, x: float, y: float, wl: float, intensity: float, z: float = 0):
        self.x = x
        self.y = y
        self.z = z
        self.wl = wl
        self.int = intensity

    def wldist(self, x, y, z):
        dist = pyta(self.x - x, self.y - y, self.z - z)
        irelative = self.int / dist ** 2
        ph = (dist - dist // self.wl) / self.wl
        return np.cos(2 * np.pi * ph) * irelative


bw = readimg.bwplaatje(fname)
EVV = np.vectorize(EV)
# create all emitter instances needed
for line in bw:
    xs = np.linspace(
        (line[0] - 0.5) * pixelsize, (line[0] + 0.5) * pixelsize, pixelamt[0]
    )
    ys = np.linspace(
        (line[1] - 0.5) * pixelsize, (line[1] + 0.5) * pixelsize, pixelamt[1]
    )
    xx, yy = np.meshgrid(xs, ys)
    emitters.extend(EVV(xx, yy, wavelength, intensity).ravel())


# use the emitters to calculate the interference on every point of the target
xs = np.linspace(-observplanesize[0] / 2, observplanesize[0] / 2, observres[0])
ys = np.linspace(-observplanesize[1] / 2, observplanesize[1] / 2, observres[1])
xx, yy = np.meshgrid(xs, ys)
plt.pcolormesh(
    xx, yy, abs(sum([o.wldist(xx, yy, observplanez) for o in emitters])), cmap=cmap
)
plt.colorbar()
plt.show()
