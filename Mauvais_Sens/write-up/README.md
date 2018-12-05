# Write up

En analysant rapidement l'image, on remarque en premier lieu qu'il s'agit d'un **BMP** avec une **palette 256 couleurs** qui ressemble à un simple niveau de gris.

![Palette de l'image](write-up/Photoshop_2018-09-20_13-00-56.png)

En y regardant de plus près, on se rend compte qu'il n'y a en fait que **16 couleurs différentes**. Sur une représentation dans un tableau 16x16, chaque entrée d'une même ligne contient la même couleur (#000000 pour la première ligne, #101010 pour la seconde, etc...).

On peut donc tenter d'y appliquer une palette contenant un vrai niveau de gris pour se rendre compte qu'il y a quelque chose derrière cette palette.
![Image en niveau de gris](write-up/Photoshop_2018-09-20_13-02-25.png)
On voit clairement apparaitre les détails d'une autre image.

Le titre de l'épreuve nous indique que *quelque-chose* est dans le *mauvais sens*. Nous pouvons donc essayer d'appliquer cette idée à notre palette de couleur.

En effectuant une rotation de la palette originale sous forme de tableau 16x16, nous obtenons une palette pour laquelle chaque ligne d'entrées est identique mais avec une *forte* variation entre chaque couleur la composant.
![Palette renversée](write-up/Photoshop_2018-09-20_13-02-51.png)

Ainsi, la palette appliquée accentue les détails repérés sur le niveau de gris tout en atténuant les différences de couleurs liées à l'image original.
![Image avec la palette renversée](write-up/Photoshop_2018-09-20_13-03-42.png)

Et le flag apparait !
