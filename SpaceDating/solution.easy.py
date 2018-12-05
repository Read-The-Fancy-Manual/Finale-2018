#!/usr/bin/env python3

import re
import sys
import numpy as np
import sklearn.linear_model as sklinear
import sklearn.preprocessing as skpreprocess



def warn(*args):
    sys.stderr.write(" ".join(str(a) for a in args) + "\n")



def read_profile_train():
    profile = []
    line = input()
    while line != "":
        featname, val = line.split(":")
        featname = featname.lstrip("\t")
        val = val.lstrip(" ")

        if featname == "like":
            like = (val == "oui")
        else:
            profile.append(float(val))

        line = input()

    profile = np.array(profile)
    return profile, like



def read_profile_test():
    profile = []
    line = input()
    while line != "":
        featname, val = line.split(":")
        featname = featname.lstrip("\t")
        val = val.lstrip(" ")
        profile.append(float(val))

        line = input()

    profile = np.array(profile)
    return profile



def main():
    pop = []
    likes = []

    line = input()
    match = re.search(r'\d+', line)
    nprofiles = int(match.group(0))

    for i in range(nprofiles):
        line = input()
        assert line.startswith("Profil")

        profile, like = read_profile_train()
        pop.append(profile)
        likes.append(like)

    pop = np.array(pop)
    likes = np.array(likes)

    classifier = sklinear.LogisticRegression(C=1000, tol=1e-6, class_weight="balanced")
    classifier.fit(pop, likes)



    line = input()
    match = re.search(r'\d+', line)
    nprofiles = int(match.group(0))
    warn(input())

    for i in range(nprofiles):
        line = input()
        assert line.startswith("Profil")

        profile = read_profile_test()
        profile = profile.reshape((1, -1))

        pred = classifier.predict(profile)[0]
        print("NO"[pred])

        result = input()

    while True:
        try:
            line = input()
        except EOFError:
            break

        warn(line)



if __name__ == '__main__':
    main()
