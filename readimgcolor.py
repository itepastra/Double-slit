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
    nim = np.array(im)
    r = np.argwhere(nim[:, :, 0] > 128)
    i = np.array([nim[r[:, 0], r[:, 1], 2]]).astype("float64").T / 255
    data = np.append(r.astype("float64"), i, 1)
    # print(data)
    data[:, 0] -= (w - 1) / 2
    data[:, 1] -= (h - 1) / 2
    data[:, 1] *= -1

    return data
