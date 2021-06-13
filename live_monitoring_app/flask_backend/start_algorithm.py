import sys
from threading import Thread

startAlgo = True

def startAlgo():
    global startAlgo
    while startAlgo:
        print("algorithm started")


def stopAlgo():
    startAlgo = False
    print("algorithm stop called")
