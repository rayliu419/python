import sys


class DoorKeeper:
    def __init__(self):
        return

    @staticmethod
    def guard():
        answer = input("WARNING: The program will add/remove data in env, are you sure to run it?")
        print("Your answer is {}".format(answer))
        if answer != "y":
            print("The answer is not y, exit")
            sys.exit(0)