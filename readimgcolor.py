import numpy as np
from PIL import Image
import os


def filepath(
    filename,
):  # deze functie geeft het path van het bestand zelf terug hoe je het ook uitvoert, zodat het programma het bestand goed kan vinden
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, filename)


def bwplaatje(fname):
    # hier openen we een plaatje
    im = Image.open(filepath(fname), "r")
    w, h = im.size
    print(w, h)
    # we maken een numpy array van de pixelwaarden in het plaatje
    nim = np.array(im)
    # waar een pixel rood genoeg is zien we als een opening in de slit
    r = np.argwhere(nim[:, :, 0] > 128)
    # het blauwe deel van de pixel bepaalt de relatieve intensiteit op dat punt
    i = np.array([nim[r[:, 0], r[:, 1], 2]]).astype("float64").T / 255
    # het groene deel doet op dit moment niets, maar deze zou kunnen worden gebruikt voor een faseverschuiving
    data = np.append(r.astype("float64"), i, 1)
    # hier draaien we de data om en maken we het midden van het plaatje het coordinaat (0,0)
    data[:, 0] -= (h - 1) / 2
    data[:, 1] -= (w - 1) / 2
    data[:, 0] *= -1
    return data
