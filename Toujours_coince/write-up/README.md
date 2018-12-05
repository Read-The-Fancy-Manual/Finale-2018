# Write up

Comme indiqué dans la description, nous allons devoir réparer un jeu de gameboy en fonction des indications données par le jeu lui-même. Il va donc falloir procéder par étape.

## Le déplacement

Dès l'ouverture du jeu, nous nous rendons compte que notre personnage ne peut bouger (un message nous en informe d'ailleurs assez clairement). Ce sera sans doute la première chose à patcher dans le jeu.  

En ouvrant le debugger, on peut voir que l'on est bloqué sur cette portion de code :  
```
  00:01F1                  ld   hl,C004
  00:01F4                  push hl
  00:01F5                  call 085B
  00:01F8               -> jr   01F8
  00:01FA                  ld   a,(C002)
  00:01FD                  nop  
  00:01FE                  ld   (C002),a
  00:0201                  ret  
```
On est a l'intérieur d'une sous-routine infinie. On peut remarquer un push (0xC004) suivi d'un call avant la boucle infinie (jump sur le PC). Ce qui suit est en revanche plus intéressant : le chargement d'un élément, un nop et la sauvegarde dudit élément. Le nop semble remplacer une instruction disparue.  
On peut donc en déduire que le push et le call servent à afficher le message (le push étant sans doute la chaine de caractères en paramètre), la boucle infinie bloque le jeu dans cet état et le reste de la routine est logiquement lié à la gestion du mouvement du personnage. Il faut donc supprimer l'affichage du message et la boucle infinie mais aussi ajouter le déplacement du joueur :
```
  00:01F1                  nop
  00:01F2                  nop
  00:01F3                  nop
  00:01F4                  nop
  00:01F5                  nop
  00:01F6                  nop
  00:01F7                  nop
  00:01F8                  nop
  00:01F9                  nop
  00:01FA                  ld   a,(C002)
  00:01FD                  inc  a
  00:01FE                  ld   (C002),a
  00:0201                  ret  
```
Et voilà, il n'y a plus qu'à faire de même pour le mouvement dans l'autre direction (`dec a`).

## La porte

Maintenant que nous pouvons nous déplacer, nous allons pouvoir aller à la porte. Malheureusement, nous arrivons à un endroit peu accueillant. On apprend que nous ne sommes pas dans le bon niveau (nommé niveau 3) et que c'est sans doute lié à la porte du niveau 1. Soit, allons étudier ça de prêt !  
Nous avons de la chance, quelques informmations symboliques sont là pour nous aider. Nous avons entre-autre des adresses nommées "levelX" et "initMap0X" (où X est une valeur de 1 à 3). Voyons le dump du level1 :
```
level1: (0279)             ld   a,20
  00:027B                  call 09CA
  00:027E                  bit  0,b
  00:0280                  jr   nz,0285
  00:0282                  call 01F1
  00:0285                  bit  1,b
  00:0287                  jr   nz,028C
  00:0289                  call 0202
  00:028C                  bit  2,b
  00:028E                  jr   nz,02B9
  00:0290                  ld   hl,FF43
  00:0293                  ld   a,(hl)
  00:0294                  ld   b,a
  00:0295                  ld   a,(C002)
  00:0298                  add  b
  00:0299                  cp   a,88
  00:029B                  jr   z,02B9
  00:029D                  jr   c,02B9
  00:029F                  cp   a,90
  00:02A1                  jr   nc,02B9
  00:02A3                  call 096B
  00:02A6                  nop  
  00:02A7                  nop  
  00:02A8                  call initMap03
  00:02AB                  ld   a,03
  00:02AD                  nop  
  00:02AE                  nop  
  00:02AF                  ld   (C001),a
  00:02B2                  ld   a,00
  00:02B4                  ld   (ff00+43),a
  00:02B6                  call 0984
  00:02B9                  call 0213
  00:02BC                  call 09AF
  00:02BF                  ret  
```
Inutile de rentrer dans le détail pour voir que ce qui pose problème est entouré de `nop nop`. Essayons de changer cette portion en :
```
  00:02A6                  nop  
  00:02A7                  nop  
  00:02A8                  call initMap02
  00:02AB                  ld   a,02
  00:02AD                  nop  
  00:02AE                  nop  
```
On relance la ROM et bingo, la porte nous mène désormais au bon niveau.

## Le scrolling

Un fois dans le niveau, on tente de se déplacer vers la droite de l'écran et là, surprise, pas de scrolling mais un petit message. Soit, procédons comme pour le déplacement :
```
  00:0213                  ld   a,(C002)
  00:0216                  cp   a,A9
  00:0218                  jr   c,0223
  00:021A                  ld   hl,C025
  00:021D                  push hl
  00:021E                  call 085B
  00:0221               -> jr   0221
  00:0223                  nop  
  00:0224                  nop  
  00:0225                  nop  
  00:0226                  nop  
  00:0227                  nop  
  00:0228                  nop  
  00:0229                  nop  
  00:022A                  nop  
  00:022B                  nop  
  00:022C                  nop  
  00:022D                  nop  
  00:022E                  nop  
  00:022F                  nop  
  00:0230                  nop  
  00:0231                  nop  
  00:0232                  nop  
  00:0233                  nop  
  00:0234                  nop  
  00:0235                  nop  
  00:0236                  nop  
  00:0237                  nop  
  00:0238                  nop  
  00:0239                  nop  
  00:023A                  nop  
  00:023B                  nop  
  00:023C                  nop  
  00:023D                  nop  
  00:023E                  nop  
  00:023F                  nop  
  00:0240                  nop  
  00:0241                  nop  
  00:0242                  nop  
  00:0243                  ret  
```
Voilà qui n'est pas très rassurant : autant de `nop` nous laisse penser que le patch sera plutôt conséquent cette fois-ci.  
Déjà un peu d'analyse. La première instruction charge le même élément que lors du déplacement : la position de notre joueur. les deux instructions suivantes effectuent un saut vers les `nop`s si la position du joueur est inférieur à 0xA9. Le cas échéant, le message est affiché comme vu précédement.  
Le message nous laisse penser qu'il faut gérer le scrolling de la gameboy. Il va donc falloir aller jeter un oeil aux [pandocs](http://bgb.bircd.org/pandocs.htm). L'information que nous cherchons se trouve ici :
```
FF42 - SCY - Scroll Y (R/W)
FF43 - SCX - Scroll X (R/W)
Specifies the position in the 256x256 pixels BG map (32x32 tiles) which is to be displayed at the upper/left LCD display position.
Values in range from 0-255 may be used for X/Y each, the video controller automatically wraps back to the upper (left) position in BG map when drawing exceeds the lower (right) border of the BG map area.
```
Il nous faut donc assigner la valeur du scrolling souhaité au byte à l'adresse 0xFF43. Le reste n'est que de l'algo. par exemple :
```
  00:0213                  ld   a,(C002)	; Récupérer la position du joueur
  00:0216                  cp   a,80		; Comparaison à 0x80
  00:0218                  jr   c,0224		; Si supérieur :
  00:021A                  dec  a			;  | Décrémenter la position du joueur
  00:021B                  ld   (C002),a	;  | Sauvegarder la position du joueur
  00:021E                  ld   hl,FF43		;  | Récupérer l'adresse du scrolling
  00:0221                  ld   a,(hl)		;  | Lire la valeur du scrolling
  00:0222                  inc  a			;  | Incrémenter le scrolling
  00:0223                  ld   (hl),a		;  | Sauvegarder la valeur du scrolling
  00:0224                  ld   a,(C002)	; Récupérer la position du joueur
  00:0227                  cp   a,30		; Comparaison à 0x30
  00:0229                  jr   nc,0235		; Si inférieur :
  00:022B                  inc  a			;  | Incrémenter la position du joueur
  00:022C                  ld   (C002),a	;  | Sauvegarder la position du joueur
  00:022F                  ld   hl,FF43		;  | Récupérer l'adresse du scrolling
  00:0232                  ld   a,(hl)		;  | Lire la valeur du scrolling
  00:0233                  dec  a			;  | Décrémenter le scrolling
  00:0234                  ld   (hl),a		;  | Sauvegarder la valeur du scrolling
  00:0235                  nop  
  00:0236                  nop  
  00:0237                  nop  
  00:0238                  nop  
  00:0239                  nop  
  00:023A                  nop  
  00:023B                  nop  
  00:023C                  nop  
  00:023D                  nop  
  00:023E                  nop  
  00:023F                  nop  
  00:0240                  nop  
  00:0241                  nop  
  00:0242                  nop  
  00:0243                  ret  
```
Et voilà, un bon scrolling fonctionnel.

## Le code

Nous arrivons ainsi à la dernière étape, le code sur le mur.  
On peut voir 4 tableau sur le mur contenant des chiffres aléatoires, un panneau nous indiquant qu'appuyer sur A regénère le code, et une porte qui ne s'ouvrira que si le code des tableau est 1337 "à chaque fois"... Il est donc envisageable que notre dernière étape soit de patcher une fonction random pour qu'elle nous génère une suite de nombre souhaitée.  
Analysons le code du level2, il est plus long que les précédent mais une séction attire l'oeil :
```
  00:0368                  ld   c,04
  00:036A                  ld   d,34
  00:036C                  call 0244
  00:036F                  ld   h,99
  00:0371                  ld   l,d
  00:0372                  ld   a,b
  00:0373                  add  a,89
  00:0375                  ldi  (hl),a
  00:0376                  inc  d
  00:0377                  inc  d
  00:0378                  inc  d
  00:0379                  dec  c
  00:037A                  jr   nz,036C
```
Une boucle itérant sur 4 éléments. Intéressant étant donné que nous cherchons à étudier le comportement de 4 tableaux. Un point d'arrêt sur la première instruction nous permet de confirmer qu'il s'agit de la routine après l'appuis sur le bouton A.  
Aucune des instructions présentes ne semblent gérer de l'aléatoire, il ne peut donc être gérer qu'à l'intérieur du seul et unique call.
```
  00:0244                  ld   hl,FF04
  00:0247                  ld   a,(hl)
  00:0248                  add  a,09
  00:024A                  sub  a,09
  00:024C                  cp   a,0A
  00:024E                  jr   nc,024A
  00:0250                  ld   b,a
  00:0251                  ld   a,(C000)
  00:0254                  inc  a
  00:0255                  ld   (C000),a
  00:0258                  nop  
  00:0259                  nop  
  00:025A                  nop  
  00:025B                  nop  
  00:025C                  nop  
  00:025D                  nop  
  00:025E                  nop  
  00:025F                  nop  
  00:0260                  nop  
  00:0261                  nop  
  00:0262                  nop  
  00:0263                  nop  
  00:0264                  nop  
  00:0265                  nop  
  00:0266                  nop  
  00:0267                  nop  
  00:0268                  nop  
  00:0269                  nop  
  00:026A                  nop  
  00:026B                  nop  
  00:026C                  nop  
  00:026D                  nop  
  00:026E                  nop  
  00:026F                  nop  
  00:0270                  nop  
  00:0271                  nop  
  00:0272                  nop  
  00:0273                  nop  
  00:0274                  nop  
  00:0275                  nop  
  00:0276                  nop  
  00:0277                  nop  
  00:0278                  ret  
```
Encore un tas de `nop`s, c'est bien ainsi que notre patch doit être effectué.
Brièvement, le code ci-dessus effectue une lecture de la valeur à l'adresse 0xFF04, lui applique un modulo 10 et sauvegarde le résultat dans le registre b. D'après les pandocs :
```
FF04 - DIV - Divider Register (R/W)
This register is incremented at rate of 16384Hz (~16779Hz on SGB). In CGB Double Speed Mode it is incremented twice as fast, ie. at 32768Hz. Writing any value to this register resets it to 00h.
```
Voilà qui explique les valeurs pseudo aléatoire. Cependant, on peut voir 3 instructions à la suite de ce code et au dessus des `nop`s qui ne semble pas avoir d'utilité. Elles chargent une valeur, l'incrémente, puis la sauvegarde.  
Super, ce code va nous aider pour notre patch : il nous permettra de connaitre combien de fois que la fonction a été appeler et ainsi retourner la valeur correspondante à ce qui est attendu (1, 3, 3 ou 7). De plus, on a un exemple de modulo si besoin est !
```
  00:0244                  ld   a,(C000)
  00:0247                  inc  a
  00:0248                  ld   (C000),a
  00:024B                  sub  a,01
  00:024D                  add  a,04
  00:024F                  sub  a,04
  00:0251                  cp   a,04
  00:0253                  jr   nc,024F
  00:0255                  cp   a,00
  00:0257                  jr   nz,025B
  00:0259                  ld   b,01
  00:025B                  cp   a,01
  00:025D                  jr   nz,0261
  00:025F                  ld   b,03
  00:0261                  cp   a,02
  00:0263                  jr   nz,0267
  00:0265                  ld   b,03
  00:0267                  cp   a,03
  00:0269                  jr   nz,026D
  00:026B                  ld   b,07
  00:026D                  nop  
  00:026E                  nop  
  00:026F                  nop  
  00:0270                  nop  
  00:0271                  nop  
  00:0272                  nop  
  00:0273                  nop  
  00:0274                  nop  
  00:0275                  nop  
  00:0276                  nop  
  00:0277                  nop  
  00:0278                  ret  
```
Le code effectue un modulo 4 de la valeur incrémentée et, en fonction du résultat, retourne 1, 3 ou 7. On peut désormais ainsi passer la porte final et obtenir le flag.
