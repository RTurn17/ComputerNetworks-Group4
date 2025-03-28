# add function to both server and client, use same setup for time

import time


def main():
    keyWord = time.time() % 8
    password = set_password(keyWord)

def set_password(loc):
    key = ["r8d4iUv43G", "sc80o1H4bM", "iWx6pMduF7", "4yV8dfX6ar", "m3C2gD8z7", "j8lnk1Egy8", "G5bl172eHv"]
    passwrd = key[loc]
    return passwrd
