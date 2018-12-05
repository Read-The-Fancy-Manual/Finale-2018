## FR:

    ### Name: "Rabbin des bois"
    ### Description: "Serez-vous capable d'injecter la bonne faute dans les bois ?"
    ### Hints: pas de hint
    ### Flag: "sigsegv{B@tm@n_@nd_R@bin}" (modifiable dans le Dockerfile)
    ### Auteur : alkanor

## EN:

    ### Name: "Rabbin hood"
    ### Description: "What if you could inject some fault in the wood ?"
    ### Hints: no hint
    ### Flag: "sigsegv{B@tm@n_@nd_R@bin}" (modifiable dans le Dockerfile)
    ### Author: alkanor


# Type de l'épreuve

Crypto : Attaque par faute sur cryptosystème Rabin (peut être résolu d'une autre manière).


# Difficulté

Moyenne. Pour ceux qui ont l'habitude de ce genre d'épreuve en CTF, ça devrait être plutôt simple.


# Epreuve

Voir la partie Makefile pour lancer l'épreuve.


# Infra requise

Aucune. Tout est contenu dans le Dockerfile.


# Test de la solution

python solution/auto_exploit.py test<br/>
python solution/auto_exploit.py # (lorsque le docker tourne)



# Makefile

cd docker<br/>
(make build # compris dans l'opération suivante)<br/>
make run

make clean # (pour supprimer tous les conteneurs et images concernés)
