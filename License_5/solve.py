"""
Ce challenge se base sur un problème de linéarité. On se place dans un espace d'ordre 2 - GF(2) - à 256 dimensions, et on récupères 256 vecteurs non colinéaires entre eux pour créer une base de cet espace.
C'est ensuite un problème linéaire (équation de matrices) pour trouver une combinaison de ces vecteurs qui permet d'atteindre n'importe quel point de cet espace.

(BASE) x (X) = (POINT)

On se retrouve avec 256 équations à 256 inconnues, ce qui se résoud via le pivot de gauss.
"""

from sage.all import *
import hashlib

GF2 = Zmod(2)

vectors, licencelines = [],[]
counter = 0

"""
Recherche de 256 vecteurs non colinéaires entre eux pour former une base
"""
while len(vectors) < 256:
    licenceline = str(counter)+"\n"
    new_vector = [reduce(lambda a, b: a+b, [[int(i) for i in "{:08b}".format(ord(byte))] for byte in hashlib.sha256(licenceline).digest()])]
    if matrix(GF2, vectors + new_vector).transpose().rank() > len(vectors):
        vectors += new_vector
        licencelines += [licenceline]
    counter+=1

"""
Création du point de l'espace à atteindre (sous forme de vecteur)
"""
KEY = reduce(lambda a, b: a+b, [[int(i) for i in "{:08b}".format(ord(c))] for c in '\x79\x24\x67\x01\xff\xe0\x6b\xd4\x66\xd8\xa7\x9f\x39\x57\x8d\x9f\x9a\x25\x31\x1d\x4c\x5d\xa6\x26\xd3\xf7\xa2\x34\x65\xc4\xf5\x1b'])

"""
Résolution de vecteurs x (X) = KEY
Puis affichage des vecteurs à garder, c'est à dire quand la coordonnées de X vaut 1.
"""
print("".join(s for x,s in zip(matrix(GF2, vectors).transpose().solve_right(vector(KEY)), licencelines) if x))
