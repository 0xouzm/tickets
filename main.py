from welcome import *
from query_tickets import *


def main():
    choice = DengLu()
    if choice == 1:
        user = YanZheng()

    if choice == 0:
        searchWindow()

if __name__ == '__main__':
    main()
