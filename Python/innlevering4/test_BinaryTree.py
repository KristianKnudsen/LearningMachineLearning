from math import floor

import pytest

from BinaryTree import BinaryTree
from BinaryTreeNode import BinaryTreeNode
from collections import namedtuple


def test_init_data():
    root_node = BinaryTreeNode(value=next(vg()))
    tree = BinaryTree(data=root_node)
    assert tree._root == root_node


def test_init_data_type_check():
    root_node = "Not a BinaryTreeNode"
    tree = BinaryTree(data=root_node)
    assert tree._root != root_node


def test_insert_root():
    tree = BinaryTree()
    tree_node = BinaryTreeNode(value=next(vg()))
    tree.insert(treenode=tree_node)
    assert tree._root == tree_node


# getnodes Variables:
# Current keeps track of which part of the binary tree you're working with. Usually root. Maybe.
# treenode should be of class BinaryTreeNode however only checks if it has a value attribute.
# if a treenode is given it should contain a value of some sort.
# if no treenode is given it will generate its own based on the given value.
def test_getnodes_given_current_treenode(it):
    tree = BinaryTree(data=BinaryTreeNode(next(it)))
    tree_node = BinaryTreeNode(next(it))
    assert tree._getnodes(current=tree._root, treenode=tree_node) == (tree._root, tree_node)


def test_getnodes_no_value_no_treenode(it):
    tree = BinaryTree(data=BinaryTreeNode(next(it)))
    with pytest.raises(Exception, match="Attempt to insert an empty space into Binary Tree"):
        tree._getnodes(current=tree._root)


# Redundant test as it tests the same if sentence as the "test_getnodes_no_value_no_treenode" method.
# The if treenode.value == None can never be true seeing as treenode == None checks the same thing.
# The dunder method __eq__ of BindaryTreeNode checks based on value which means the comparison becomes redundant.
def test_getnodes_no_value_no_current_no_treenodevalue():
    tree = BinaryTree()
    tree_node = BinaryTreeNode(value=None)
    with pytest.raises(Exception, match="Attempt to insert an empty space into Binary Tree"):
        tree._getnodes(treenode=tree_node)


def test_getnodes_treenode_value_no_current(it):
    tree = BinaryTree(data=BinaryTreeNode(next(it)))
    tree_node = BinaryTreeNode(value=next(it))
    with pytest.raises(Exception, match="Key inconsistency detected"):
        tree._getnodes(treenode=tree_node, value=next(it))


def test_getnodes_current_value_no_treenode(it):
    root = next(it)
    value = next(it)
    treenode_out = BinaryTreeNode(value=value)
    root_node = BinaryTreeNode(value=root)
    tree = BinaryTree(data=root_node)
    assert tree._getnodes(current=root_node, value=value) == (root_node, treenode_out)


def test_getnodes_value_no_current_no_treenode(it):
    root = next(it)
    value = next(it)
    treenode_out = BinaryTreeNode(value=value)
    root_node = BinaryTreeNode(value=root)
    tree = BinaryTree(data=root_node)
    assert tree._getnodes(value=value) == (root_node, treenode_out)


# Insert testing continues

# Due to the getnodes method the insert method wont work given both treenode and value
# Get node is already tested, but for demostration
def test_insert_treenode_value_no_current(it):
    tree = BinaryTree()
    tree_node = BinaryTreeNode(value=next(it))
    with pytest.raises(Exception, match="Key inconsistency detected"):
        tree.insert(value=next(it), treenode=tree_node)


# Generates two unique values and puts them in a sorted list
# Puts the bigger value as the root node and sees if the insert method places
# The smaller value at the right place
def test_insert_current_value_less_no_treenode(it):
    values = [next(it), next(it)]
    values.sort()
    root_node = BinaryTreeNode(values[1])
    tree = BinaryTree(data=root_node)
    tree.insert(current=root_node, value=values[0])
    assert root_node.left.value == values[0]


# Does the same as the one before except adds another layer
# .left.left could probably be replace with findleftmost
def test_insert_value_less_2levels_no_treenode_no_current(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    root_node = BinaryTreeNode(values[2])
    root_node.left = BinaryTreeNode(values[1])
    tree = BinaryTree(data=root_node)
    tree.insert(value=values[0])
    assert root_node.left.left.value == values[0]


def test_insert_value_more_2levels_no_treenode_no_current(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    root_node = BinaryTreeNode(values[0])
    root_node.right = BinaryTreeNode(values[1])
    tree = BinaryTree(data=root_node)
    tree.insert(value=values[2])
    assert root_node.right.right.value == values[2]


def test_insert_value_not_more_or_less_no_root(it):
    tree_node = BinaryTreeNode(value=next(it))
    tree = BinaryTree()
    tree.insert(current=tree_node, treenode=tree_node)
    assert tree._root == tree_node


# Kinda stupid but works
# The treenode value needs to be convertible to a string which namedtuple is not by default.
# Therefore a without changing the datatype i just used a string instead.
# The program will raise a TypeError exception instead if it cant convert.
def test_insert_value_not_more_or_less_root(it):
    tree_node = BinaryTreeNode(value="next(it)")
    root_node = BinaryTreeNode(value=next(it))
    tree = BinaryTree(data=root_node)
    with pytest.raises(Exception, match="Duplicate key"):
        tree.insert(current=tree_node, treenode=tree_node)


def test_find_key_bigger_no_treenode(it):
    values = [next(it), next(it)]
    values.sort()
    tree_node1 = BinaryTreeNode(value=values[0])
    tree_node2 = values[1]
    tree = BinaryTree(data=tree_node1)
    tree.insert(value=tree_node2)
    result = tree.find(tree_node2)
    assert result.value == tree_node2


def test_find_key_smaller_no_treenode(it):
    values = [next(it), next(it)]
    values.sort()
    tree_node1 = BinaryTreeNode(value=values[1])
    tree_node2 = values[0]
    tree = BinaryTree(data=tree_node1)
    tree.insert(value=tree_node2)
    result = tree.find(tree_node2)
    assert result.value == tree_node2


def test_find_key_no_rootvalue_no_treenode(it):
    tree_node1 = BinaryTreeNode(next(it))
    tree = BinaryTree()
    result = tree.find(tree_node1)
    assert result is None


def test_find_max(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    root_node = BinaryTreeNode(value=values[0])
    tree = BinaryTree(data=root_node)
    tree.insert(value=values[1])
    tree.insert(value=values[2])
    result = tree.findMax()
    assert BinaryTreeNode(value=values[2]) == result


def test_rightmost(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    root_node = BinaryTreeNode(value=values[0])
    tree = BinaryTree(data=root_node)
    tree.insert(value=values[1])
    tree.insert(value=values[2])
    result = tree.findRightMost(root_node)
    assert BinaryTreeNode(value=values[2]) == result


def test_find_min(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    root_node = BinaryTreeNode(value=values[2])
    tree = BinaryTree(data=root_node)
    tree.insert(value=values[1])
    tree.insert(value=values[0])
    result = tree.findMin()
    assert BinaryTreeNode(value=values[0]) == result


def test_find_leftmost(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    root_node = BinaryTreeNode(value=values[2])
    tree = BinaryTree(data=root_node)
    tree.insert(value=values[1])
    tree.insert(value=values[0])
    result = tree.findLeftMost(root_node)
    assert BinaryTreeNode(value=values[0]) == result


def test_delete_min_smallest_first(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    tree = BinaryTree()
    tree_node = BinaryTreeNode(value=values[1])
    tree.insert(value=values[0])
    tree.insert(treenode=tree_node)
    tree.insert(value=values[2])
    tree.deleteMin()
    result = tree.findMin()
    assert result.value == tree_node.value


def test_delete_min_smallest_last(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    tree = BinaryTree()
    tree_node = BinaryTreeNode(value=values[0])
    tree.insert(value=values[2])
    tree.insert(value=values[1])
    tree.insert(value=values[0])
    result = tree.deleteMin()
    assert result.value == tree_node.value


def test_delete_min_lagre_order_smallest_middle(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    tree = BinaryTree()
    tree_node = BinaryTreeNode(value=values[0])
    tree.insert(value=values[2])
    tree.insert(value=values[0])
    tree.insert(value=values[1])
    result = tree.deleteMin()
    assert result.value == tree_node.value


def test_delete_max_smallest_first(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    tree = BinaryTree()
    tree_node = BinaryTreeNode(value=values[1])
    tree.insert(value=values[0])
    tree.insert(treenode=tree_node)
    tree.insert(value=values[2])
    tree.deleteMax()
    result = tree.findMax()
    assert result.value == tree_node.value


def test_delete_max_smallest_first_middle_last(it):
    values = [next(it), next(it), next(it)]
    values.sort()
    tree = BinaryTree()
    tree_node = BinaryTreeNode(value=values[2])
    tree.insert(value=values[0])
    tree.insert(value=values[2])
    tree.insert(value=values[1])
    result = tree.deleteMax()
    assert result.value == tree_node.value


def test_delete_root_without_children():
    root_value = next(vg())
    root_node = BinaryTreeNode(value=root_value)
    tree = BinaryTree(data=root_node)
    result = tree.delete(root_value)
    assert result == root_node


def test_delete_root_with_two_children(it):
    values = [next(it), next(it), next(it)]
    root_node = BinaryTreeNode(value=values[1])
    child_node = BinaryTreeNode(value=values[0])
    tree = BinaryTree(data=root_node)
    tree.insert(treenode=child_node)
    tree.insert(value=values[2])
    result = tree.delete(values[1])
    assert result == root_node


def test_delete_lesser_child(it):
    values = [next(it), next(it)]
    root_node = BinaryTreeNode(value=values[1])
    child_node = BinaryTreeNode(value=values[0])
    tree = BinaryTree(data=root_node)
    tree.insert(treenode=child_node)
    result = tree.delete(values[0])
    assert result == child_node


def test_delete_greater_child(it):
    values = [next(it), next(it)]
    root_node = BinaryTreeNode(value=values[0])
    child_node = BinaryTreeNode(value=values[1])
    tree = BinaryTree(data=root_node)
    tree.insert(treenode=child_node)
    result = tree.delete(values[1])
    assert result == child_node


def test_delete_greater_child_with_lesser_child(it):
    values = [next(it), next(it), next(it)]
    root_node = BinaryTreeNode(value=values[0])
    child_node = BinaryTreeNode(value=values[2])
    grandchild_node = BinaryTreeNode(value=values[1])
    tree = BinaryTree(data=root_node)
    tree.insert(treenode=child_node)
    tree.insert(treenode=grandchild_node)
    result = tree.delete(values[2])
    assert result == child_node


def test_delete_greater_child_with_greater_child(it):
    values = [next(it), next(it), next(it)]
    root_node = BinaryTreeNode(value=values[0])
    child_node = BinaryTreeNode(value=values[1])
    grandchild_node = BinaryTreeNode(value=values[2])
    tree = BinaryTree(data=root_node)
    tree.insert(treenode=child_node)
    tree.insert(treenode=grandchild_node)
    result = tree.delete(values[1])
    assert result == child_node


def test_delete_lesser_child_with_lesser_child(it):
    values = [next(it), next(it), next(it)]
    root_node = BinaryTreeNode(value=values[2])
    child_node = BinaryTreeNode(value=values[1])
    grandchild_node = BinaryTreeNode(value=values[0])
    tree = BinaryTree(data=root_node)
    tree.insert(treenode=child_node)
    tree.insert(treenode=grandchild_node)
    result = tree.delete(values[1])
    assert result == child_node


def test_delete_lesser_child_with_greater_child(it):
    values = [next(it), next(it), next(it)]
    root_node = BinaryTreeNode(value=values[2])
    child_node = BinaryTreeNode(value=values[0])
    grandchild_node = BinaryTreeNode(value=values[1])
    tree = BinaryTree(data=root_node)
    tree.insert(treenode=child_node)
    tree.insert(treenode=grandchild_node)
    result = tree.delete(values[0])
    assert result.value == values[0]


def test_delete_root_big_tree(it):
    values = []
    counter = 0
    root = next(it)
    values.append(root)
    while counter < 99:
        values.append(next(it))
        counter += 1
    values.sort()
    counter = 0
    tree = BinaryTree()
    while counter < 100:
        tree.insert(value=values[counter])
        counter += 1
    result = tree.delete(root)
    assert result.value == root


# Binary tree balanced insert order
# Takes a sorted list and returns an insert order which creates a balanced search tree.
def btbio(lst: list) -> list:
    ll = len(lst)
    mid = int(ll / 2)
    if ll <= 2:
        return lst
    return [lst[mid]] + btbio(lst[:mid]) + btbio(lst[mid + 1:])


# Value generator for binary tree
# Limit is 100000 values
# If all the tests fail this is likly the cause
def vg() -> namedtuple:
    with open("Personer.dta") as file:
        info = namedtuple("info", "last first address postcode city")
        for line in file:
            line_list = line.strip().split(";")
            line_namedtuple = info(*line_list)
            yield line_namedtuple


# Could create more fixtures for generating values array with
# sorted values.
@pytest.fixture()
def it():
    return vg()
