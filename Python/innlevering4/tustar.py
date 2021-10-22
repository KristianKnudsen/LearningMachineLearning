import pytest

from BinaryTree import BinaryTree
from BinaryTreeNode import BinaryTreeNode
from collections import namedtuple


# Value generator for binary tree
# Limit is 100000 values
def vg():
    with open("Personer.dta") as file:
        info = namedtuple("info", "last first address postcode city")
        for line in file:
            line_list = line.strip().split(";")
            line_namedtuple = info(*line_list)
            yield line_namedtuple



def create_tree():
    return None


if __name__ == "__main__":
    lst = []
    counter = 0
    while counter < 16:
        lst.append(counter)
        counter += 1

    mid = int(len(lst)/2)
    print(btbio(lst))
