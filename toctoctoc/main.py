import os
import re
import shutil
import flag
import time

def del_folder(path):
    root_folder = '/'.join(path.split('/')[0:3])
    shutil.rmtree(root_folder)

def main():
    folder_name = input('nom du dossier, min 5 lettres): ')
    path = os.path.abspath('/tmp/' + str(folder_name)).strip() + '/'
    if os.path.abspath(path)[:5] == '/tmp/' and len(path) > 10:
        # just to be sure that we are writing in /tmp/
        try:
            os.makedirs(path)
            # spamming the disk to ensure that SigSegV1 is the best hacking event ever
            for i in range(0, 30000):
                f = open(path + str(i) + '.txt', 'w+')
                f.write('SigSegV1 is the best hacking event ever')
                f.close()

            files = os.listdir(path)
            for f in files:
                if 'pwned' in f:
                    flag.print_flag()
                    break
            del_folder(path)

        except Exception as e:
            # in case something fails, we wait a few secondes & clean path
            t0 = time.time()
            print('Ooops. Echec critique. Le dossier existe peut etre deja.')
            while(t0 + 2 > time.time()):
                time.sleep(1)
                continue
            del_folder(path)
    else:
        print('Le dossier doit etre dans /tmp/ et faire 5+ chars')

if __name__ == "__main__":
    main()
