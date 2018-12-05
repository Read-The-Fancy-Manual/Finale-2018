FR:
    - Name: "SpaceDating"
    - Description: "Data scientist chez SpaceDating, aidez des aliens à
    rencontrer l'amour.

    L'application SpaceDating permet aux utilisateur de *liker* ou d'écarter
    les profiles d'autres utilisateurs. À partir des informations de profiles
    likés ou écartés, trouvez d'autres profiles pertinents à proposer."

    Fournir au challenger: La description, l'IP et port du serveur.
    Si nécessaire, le deuxième hint est le code de l'épreuve. Attention à
    donner le fichier server.easy.py si c'est la version easy qui est choisie.

    - Hints:
	- "Un peu de logistique peut-être ?"
        - Le fichier [server.py](server.py) (sans le flag, obviously)
    - Flag: "sigsegv{I_L0v3_Tent4cl3s}"

    - Solution: utiliser socat pour lancer le programme (changer l'adresse IP
    et le port si nécessaire).
        - socat TCP:127.0.0.1:6969 EXEC:./solution.easy.py

EN:
    - Name: "SpaceDating"
    - Description: "Data scientist at SpaceDating, help aliens to find love.

    The SpaceDating app allows users to like or discard the profile of other
    users. From the informations in the liked or discarded profiles, your job
    is to find more relevant profiles for a given user."
    - Hints:
	- "Need some logistic?"
        - [server.py](server.py)
    - Flag: "sigsegv{I_L0v3_Tent4cl3s}"

    - Solution: Use socat to run the program (change the IP address and port if
    necessary).
        - socat TCP:127.0.0.1:6969 EXEC:./solution.easy.py
