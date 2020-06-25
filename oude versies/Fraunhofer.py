import cmath
import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib as mpl
import readimgcolor

fname = "test1.png"
wavelength = 500e-9
pixelsize = (0.05e-3, 0.5e-3)
pixelamt = (5, 5)
intensity = 1
emitters = np.array([0, 0, 0, 0])
observplanez = 3.05e0
observplanesize = (5e-1, 5e-1)
observres = (400, 400)
cmap = mpl.cm.cool
k = 2 * np.pi / wavelength
c = 299792458

B = lambda l, m, x, y, i: i * np.exp(1j * (k * c - k * (l * x + m * y)))
C = lambda a, b: np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def U(x, y, z):
    co = np.array([x, y, z])
    e1 = np.array([1, 0, 0])
    e2 = np.array([0, 1, 0])
    b = np.zeros_like(x, dtype="complex128")
    print(len(emitters))
    for n, emitter in enumerate(emitters):
        b += B(C(co, e1), C(co, e2), emitter[0], emitter[1], emitter[2])
        if n % 10 == 0:
            print(n)
    return b * pixelsize[0] / pixelamt[0] * pixelsize[1] / pixelamt[1]


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
        hstack = np.column_stack(
            (x, y, np.full_like(x, line[2] * intensity), np.full_like(x, line[1]))
        )
        emitters = np.vstack((emitters, hstack))
print(emitters)
print(f"{len(emitters)} emitters have been created")


# use the emitters to calculate the interference on every point of the target
xs = np.linspace(-observplanesize[0] / 2, observplanesize[0] / 2, observres[0])
ys = np.linspace(-observplanesize[1] / 2, observplanesize[1] / 2, observres[1])
xx, yy = np.meshgrid(xs, ys)
print(f"meshgrid of size {observres[0]} by {observres[1]} has been made")
s = U(xx, yy, observplanez)
I = np.real_if_close(s * np.conjugate(s))
plt.pcolormesh(xx, yy, I, cmap=cmap)
plt.colorbar()
plt.show()
