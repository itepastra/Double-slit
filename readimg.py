import numpy as np
from PIL import Image
import os


def filepath(
    filename,
):  # deze functie geeft het path van het bestand zelf terug hoe je het ook uitvoert, zodat het programma het bestand goed kan vinden
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, filename)


def bwplaatje(fname):
    im = Image.open(filepath(fname), "r")
    w, h = im.size
    print(w, h)
    gray = im.convert("L")
    bw = np.argwhere(np.array(gray) < 128)
    fbw = bw.astype("float64")
    fbw[:, 0] -= (w - 1) / 2
    fbw[:, 1] -= (h - 1) / 2
    fbw[:, 1] *= -1
    print(bw, fbw)
    return fbw
