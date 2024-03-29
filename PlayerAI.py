import pygame
import random

from connect_4 import CR_GREEN, CR_RED

DEEP = 5


def max_list(l_in):
    l_out = []
    for item in l_in:
        if len(l_out) == 0 or item[0] > l_out[0][0]:
            l_out = [item]
        elif item[0] == l_out[0][0]:
            l_out.append(item)

    return l_out


def min_list(l_in):
    l_out = []
    for item in l_in:
        if len(l_out) == 0 or l_out[0][0] > item[0]:
            l_out = [item]
        elif item[0] == l_out[0][0]:
            l_out.append(item)

    return l_out


def get_next_move_owner(current_owner):
    next_move_owner = 'DUMMY'
    if current_owner == 'COMPUTER':
        next_move_owner = 'PLAYER'
    elif current_owner == 'PLAYER':
        next_move_owner = 'COMPUTER'
    return next_move_owner


class Button:

    def __init__(self, owner, position, radius) -> None:
        self._owner = owner
        self._position = position
        self._radius = radius
        if self._owner == 'PLAYER':
            self._color = CR_RED
        else:
            self._color = CR_GREEN

    def draw(self, surface):
        pygame.draw.circle(surface, self._color, self._position, self._radius)

    def move(self, y):
        self._position[1] += y

    def __str__(self) -> str:
        return self._owner

    def __eq__(self, other: str):
        return self._owner == other


class State:
    def __init__(self, state) -> None:
        self._state = state

    def get_short(self) -> list:
        short = []
        for nr_of_col in range(len(self._state[0])):
            short.append(0)
            for nr_of_row in range(len(self._state)):
                if self._state[nr_of_row][nr_of_col] is not None:
                    short[nr_of_col] += 1
        return short

    def get(self):
        return self._state

    def get_accessible_states(self, current_owner):
        acc = []
        next_move_owner = get_next_move_owner(current_owner)
        for nr_of_col in range(len(self._state[0])):
            if self._state[len(self._state) - 1][nr_of_col] is None:
                temp_state = [row.copy() for row in self._state]
                temp_state[len(self._state) - 1][nr_of_col] = Button(next_move_owner, None, None)
                acc.append(State(temp_state))
                continue

            for nr_of_row in range(len(self._state) - 1):
                if self._state[nr_of_row][nr_of_col] is None and self._state[nr_of_row + 1][nr_of_col] is not None:
                    temp_state = [row.copy() for row in self._state]
                    temp_state[nr_of_row][nr_of_col] = Button(next_move_owner, None, None)
                    acc.append(State(temp_state))
                    break
        return acc

    def __str__(self) -> str:
        state_str = ""
        for row in self._state:
            state_str += '[\t'
            for element in row:
                state_str += str(element)
                state_str += '\t'
            state_str += ']\n'
        return state_str

    def get_column_to_new_state(self, other):
        for row_nr in range(len(self._state)):
            for col_nr in range(len(self._state[row_nr])):
                if self._state[row_nr][col_nr] != other[row_nr][col_nr]:
                    return col_nr


def h(board, columns, rows):
    heuristic_value = 0

    for nr_of_row in range(rows):
        for nr_of_col in range(columns):
            if nr_of_col + 1 < columns:
                if board[nr_of_row][nr_of_col] == 'PLAYER' and board[nr_of_row][nr_of_col + 1] == 'PLAYER':
                    heuristic_value += 10
                if board[nr_of_row][nr_of_col] == 'COMPUTER' and board[nr_of_row][nr_of_col + 1] == 'COMPUTER':
                    heuristic_value -= 10

    for nr_of_row in range(rows):
        for nr_of_col in range(columns):
            if nr_of_row + 1 < rows:
                if board[nr_of_row][nr_of_col] == 'PLAYER' and board[nr_of_row + 1][nr_of_col] == 'PLAYER':
                    heuristic_value += 10
                if board[nr_of_row][nr_of_col] == 'COMPUTER' and board[nr_of_row + 1][nr_of_col] == 'COMPUTER':
                    heuristic_value -= 10

    for nr_of_row in range(rows):
        for nr_of_col in range(columns):
            if nr_of_row + 1 < rows and nr_of_col - 1 >= 0:
                if board[nr_of_row][nr_of_col] == 'PLAYER' and board[nr_of_row + 1][nr_of_col - 1] == 'PLAYER':
                    heuristic_value += 10
                if board[nr_of_row][nr_of_col] == 'COMPUTER' and board[nr_of_row + 1][nr_of_col - 1] == 'COMPUTER':
                    heuristic_value -= 10
    for nr_of_row in range(rows):
        for nr_of_col in range(columns):
            if nr_of_col + 1 < columns and nr_of_row + 1 < rows:

                if board[nr_of_row][nr_of_col] == 'PLAYER' and board[nr_of_row + 1][nr_of_col + 1] == 'PLAYER':
                    heuristic_value += 10
                if board[nr_of_row][nr_of_col] == 'COMPUTER' and board[nr_of_row + 1][nr_of_col + 1] == 'COMPUTER':
                    heuristic_value -= 10
    for nr_of_row in range(rows):
        for nr_of_col in range(columns):
            if nr_of_col + 2 < columns:
                if board[nr_of_row][nr_of_col] == 'PLAYER' and board[nr_of_row][nr_of_col + 1] == 'PLAYER' and \
                        board[nr_of_row][nr_of_col + 2] == 'PLAYER':
                    heuristic_value += 100
                if board[nr_of_row][nr_of_col] == 'COMPUTER' and board[nr_of_row][nr_of_col + 1] == 'COMPUTER' and \
                        board[nr_of_row][nr_of_col + 2] == 'COMPUTER':
                    heuristic_value -= 100

    for nr_of_row in range(rows):
        for nr_of_col in range(columns):
            if nr_of_row + 2 < rows:
                if board[nr_of_row][nr_of_col] == 'PLAYER' and board[nr_of_row + 1][nr_of_col] == 'PLAYER' and \
                        board[nr_of_row + 2][nr_of_col] == 'PLAYER':
                    heuristic_value += 100
                if board[nr_of_row][nr_of_col] == 'COMPUTER' and board[nr_of_row + 1][nr_of_col] == 'COMPUTER' and \
                        board[nr_of_row + 2][nr_of_col] == 'COMPUTER':
                    heuristic_value -= 100

    for nr_of_row in range(rows):
        for nr_of_col in range(columns):
            if nr_of_row + 2 < rows and nr_of_col - 2 >= 0:
                if board[nr_of_row][nr_of_col] == 'PLAYER' and board[nr_of_row + 1][nr_of_col - 1] == 'PLAYER' and \
                        board[nr_of_row + 2][nr_of_col - 2] == 'PLAYER':
                    heuristic_value += 100
                if board[nr_of_row][nr_of_col] == 'COMPUTER' and board[nr_of_row + 1][nr_of_col - 1] == 'COMPUTER' and \
                        board[nr_of_row + 2][
                            nr_of_col - 2] == 'COMPUTER':
                    heuristic_value -= 100
    for nr_of_row in range(rows):
        for nr_of_col in range(columns):
            if nr_of_col + 2 < columns and nr_of_row + 2 < rows:
                if board[nr_of_row][nr_of_col] == 'PLAYER' and board[nr_of_row + 1][nr_of_col + 1] == 'PLAYER' and \
                        board[nr_of_row + 2][nr_of_col + 2] == 'PLAYER':
                    heuristic_value += 100
                if board[nr_of_row][nr_of_col] == 'COMPUTER' and board[nr_of_row + 1][nr_of_col + 1] == 'COMPUTER' and \
                        board[nr_of_row + 2][
                            nr_of_col + 2] == 'COMPUTER':
                    heuristic_value -= 100

    for nr_of_row in range(rows):
        for nr_of_col in range(columns):
            if nr_of_col + 3 < columns:
                if board[nr_of_row][nr_of_col + 1] == board[nr_of_row][nr_of_col]:
                    if board[nr_of_row][nr_of_col + 2] == board[nr_of_row][nr_of_col]:
                        if board[nr_of_row][nr_of_col + 3] == board[nr_of_row][nr_of_col]:
                            if board[nr_of_row][nr_of_col] == 'PLAYER':
                                heuristic_value += 1000
                            else:
                                heuristic_value -= 1000

                if nr_of_row + 3 < rows:
                    if board[nr_of_row + 1][nr_of_col + 1] == board[nr_of_row][nr_of_col]:
                        if board[nr_of_row + 2][nr_of_col + 2] == board[nr_of_row][nr_of_col]:
                            if board[nr_of_row + 3][nr_of_col + 3] == board[nr_of_row][nr_of_col]:
                                if board[nr_of_row][nr_of_col] == 'PLAYER':
                                    heuristic_value += 1000
                                else:
                                    heuristic_value -= 1000

            if nr_of_row + 3 < rows:
                if board[nr_of_row + 1][nr_of_col] == board[nr_of_row][nr_of_col]:
                    if board[nr_of_row + 2][nr_of_col] == board[nr_of_row][nr_of_col]:
                        if board[nr_of_row + 3][nr_of_col] == board[nr_of_row][nr_of_col]:
                            if board[nr_of_row][nr_of_col] == 'PLAYER':
                                heuristic_value += 1000
                            else:
                                heuristic_value -= 1000
                if nr_of_col - 3 >= 0:
                    if board[nr_of_row + 1][nr_of_col - 1] == board[nr_of_row][nr_of_col]:
                        if board[nr_of_row + 2][nr_of_col - 2] == board[nr_of_row][nr_of_col]:
                            if board[nr_of_row + 3][nr_of_col - 3] == board[nr_of_row][nr_of_col]:
                                if board[nr_of_row][nr_of_col] == 'PLAYER':
                                    heuristic_value += 1000
                                else:
                                    heuristic_value -= 1000
    return heuristic_value


class Node:
    def __init__(self, state, value, type, parent, owner):
        self._value = value
        self._state = state
        self._owner = owner
        self._type = type
        self._parent = parent

        self._children = []

    def get_type(self):
        return self._type

    def get_children(self):
        return self._children

    def get_parent(self):
        return self._parent

    def get_val(self):
        return self._value

    def get_state(self):
        return self._state

    def create_children(self, heuristics):
        states = self._state.get_accessible_states(self._owner)
        node_type = 'MIN' if self._type == 'MAX' else 'MAX'
        next_move_owner = get_next_move_owner(self._owner)
        for s in states:
            val = heuristics(s.get(), 7, 6) if heuristics is not None else -1
            self._children.append(Node(s, val, node_type, self, next_move_owner))
        return self._children

    def __str__(self) -> str:
        node_str = str(self._state)
        node_str += "h(state)="
        node_str += str(self._value)
        node_str += '\n'
        return node_str

    def __gt__(self, other):
        return self._value > other.get_val()

    def __eq__(self, other):
        return self._value == other.get_val()

    def __hash__(self):
        return hash(self._state)


class Tree:

    def __init__(self, root: Node):
        self._root = root
        self._tree = [
            [root],
        ]

    def construct(self, depth):
        if len(self._tree) != 1:
            return

        for i in range(1, depth):
            self._add_level(h if i == (depth - 1) else None)

    def _add_level(self, heur):
        level = []
        for node in self._tree[-1]:
            level += node.create_children(heur)
        self._tree.append(level)

    def __str__(self) -> str:
        tree_str = "============================== ROOT ===========================\n"
        tree_str += str(self._root) + '\n'
        for level in self._tree[1:]:
            tree_str += ("============================== " + str(
                self._tree.index(level)) + " ===========================\n")
            for node in level:
                tree_str += str(node)
                tree_str += '\n'

        return tree_str

    def minmax(self):
        chosen_node = None
        if len(self._tree) == 0:
            return None
        values = {}
        if len(self._tree) == 1:
            return self._tree[-1][random.randint(0, len(self._tree[-1]) - 1)]
        for parent in self._tree[-2]:
            if parent.get_type() == 'MAX':
                temp = max_list([(node, None) for node in parent.get_children()])
            else:
                temp = min_list([(node, None) for node in parent.get_children()])
            values[parent] = temp[random.randint(0, len(temp) - 1)][0].get_val()
        print(values)
        for i in range(len(self._tree) - 3, -1, -1):
            new_values = {}
            for parent in self._tree[i]:
                if parent.get_type() == 'MAX':
                    temp = max_list([(values[child], child) for child in parent.get_children()])
                else:
                    temp = min_list([(values[child], child) for child in parent.get_children()])
                new_values[parent] = temp[random.randint(0, len(temp) - 1)]
                if i == 0:
                    chosen_node = new_values[parent][1]
            values = new_values
        print(values)
        assert chosen_node is not None, "There must be chosen one node"
        return chosen_node

    def tree_height(self):
        return len(self._tree)

    def nodes_count(self):
        nodes = 0
        for level in self._tree:
            nodes += len(level)
        return nodes


class MinMaxPlayer:

    def __init__(self, is_first: bool):
        self._tree = None


if __name__ == '__main__':
    import time

    buttonDummy = Button('DUMMY', None, None)
    state = State([[None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None],
                   [buttonDummy, None, None, None, None, None, buttonDummy],
                   [buttonDummy, None, None, None, None, None, buttonDummy],
                   [buttonDummy, None, None, buttonDummy, buttonDummy, buttonDummy, buttonDummy]])
    tree = Tree(Node(state, 1, 'MAX', None, 'DUMMY'))
    start_time = time.time()
    tree.construct(4)
    print(tree)
    print(tree.minmax())
    elapsed_time = time.time() - start_time
    print(elapsed_time)
