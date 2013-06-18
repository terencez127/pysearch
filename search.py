# from memory_profiler import profile
import math
import datetime
import sys

STATE_CUTOFF = 0X111

class puzzle_state():

    def __init__(self, width, tiles=[], parent=None, g=0):
        self.tiles = tiles[:]
        self.parent = parent
        self.g_value = g
        self.width = width
        self.move_from_parent = 0

    def moves(self):
        empty = self.tiles.index(0)
        moves = []

        adjacencies = []
        # move tile above
        if empty >= self.width:
            adjacencies.append(empty - self.width)
        # move tile below
        if empty < len(self.tiles) - self.width:
            adjacencies.append(empty + self.width)
        # move left tile
        if empty % self.width != 0:
            adjacencies.append(empty - 1)
        # move right tile
        if empty % self.width != self.width - 1:
            adjacencies.append(empty + 1)

        for i in adjacencies:
            new_state = puzzle_state(self.width, self.tiles, self, self.g_value + 1)
            new_state.move_from_parent = new_state.tiles[i]
            new_state.tiles[i], new_state.tiles[empty] = new_state.tiles[empty], new_state.tiles[i]
            # if new_state not in explored:
            moves.append(new_state)

        return moves

    def h(self, table):
        distance = 0
        for i, tile in enumerate(self.tiles):
            distance += table[tile][i]
        return distance

    def isGoal(self):
        if self.tiles == range(len(self.tiles)):
            return True
        else:
            return False

    def __eq__(self, other):
        if hasattr(other, 'tiles') and self.tiles == other.tiles:
            return True
        else:
            return False

    def __hash__(self):
        return hash(tuple(self.tiles))


def best_first(w, h, initial_node, func=None):
    if initial_node.isGoal():
        return initial_node

    frontier = []
    frontier_set = set()
    frontier.append(initial_node)
    frontier_set.add(initial_node)
    explored = set()
    generated = 0
    while frontier:
        if func is None:
            node = frontier.pop(0)
            frontier_set.remove(node)
        else:
            node = sorted(frontier, key=func)[0]
            frontier.remove(node)
            frontier_set.remove(node)
        # explored.add(node)
        explored.add(hash(node))
        moves = node.moves()
        generated += len(moves)
        for move in moves:
            # if not move in frontier_set and not move in explored:
            if not move in frontier_set and not hash(move) in explored:
                if move.isGoal():
                    seq = []
                    while move.parent is not None:
                        seq[0:0] = [move.move_from_parent]
                        move = move.parent
                    return (len(explored), generated), len(seq), seq
                frontier.append(move)
                frontier_set.add(move)
    return (0,0), 0, []


def ucs(w, h, initial):
    initial = puzzle_state(w, initial)
    return best_first(w, h, initial)


def astar(w, h, initial):
    mtable = create_mahnhattan_table(w, h)
    initial = puzzle_state(w, initial)
    return best_first(w, h, initial, lambda node: node.g_value + node.h(mtable))


def greedy(w, h, initial):
    mtable = create_mahnhattan_table(w, h)
    initial = puzzle_state(w, initial)
    return best_first(w, h, initial, lambda node: node.h(mtable))


def dls(w, h, initial, depth=sys.maxint, func=None):
    frontier = []
    frontier_set = set()
    frontier.append(initial)
    frontier_set.add(initial)
    explored = set()
    generated = 0

    next_depth = sys.maxint
    explored_dict = {}
    while frontier:
        if func is None:
            node = frontier.pop(0)
            frontier_set.remove(node)
        else:
            node = sorted(frontier, key=func)[0]
            frontier.remove(node)
            frontier_set.remove(node)
        explored.add(node)
        explored_dict[hash(node)] = node.g_value

        # reach limit, cut off thie branch
        if func is None:
            if node.g_value > depth:
                continue
        else:
            new_depth = func(node)
            if new_depth > depth:
                if new_depth < next_depth:
                    next_depth = new_depth
                continue

        if node.isGoal():
            seq = []
            while node.parent is not None:
                seq[0:0] = [node.move_from_parent]
                node = node.parent
            return (len(explored), generated), len(seq), seq

        moves = []
        for move in node.moves():
            generated += 1
            if move not in explored and not move in frontier_set:
                frontier_set.add(move)
                moves.append(move)
            else:
                h = hash(move)
                if explored_dict.has_key(h) and explored_dict[h] > move.g_value:
                    explored.remove(move)
                    explored_dict[h] = 0
                    frontier_set.add(move)
                    moves.append(move)

        frontier[0:0] = moves
    return (len(explored), generated), next_depth, []


def ids(w, h, initial):
    initial_node = puzzle_state(w, initial)
    sum_tuples = []
    for i in xrange(1, 10000):
        # print i
        sum_tuple, steps, moves = dls(w, h, initial_node, i)
        sum_tuples.append(sum_tuple)
        if moves:
            return sum_tuples, steps, moves


def idastar(w, h, initial):
    mtable = create_mahnhattan_table(w, h)
    initial_node = puzzle_state(w, initial)
    limit = int(initial_node.g_value + initial_node.h(mtable))
    sum_tuples = []
    # while limit < sys.maxint:
    # for i in xrange(limit, 10000):
    #     sum_tuple, steps, moves = dls(w, h, initial_node, i, lambda state: state.g_value + state.h(mtable))
    while limit < sys.maxint:
        sum_tuple, steps, moves = dls(w, h, initial_node, limit, lambda state: state.g_value + state.h(mtable))
        sum_tuples.append(sum_tuple)
        if moves:
            return sum_tuples, steps, moves
        else:
            limit = steps


# Utilities
def create_mahnhattan_table(w, h):
    r = w * h
    mtable = [[0 for i in range(r)] for j in range(r)]
    for tile in xrange(r):
        if tile != 0:
            dest_col = tile % w
            dest_row = tile / w
            for pos in xrange(r):
                if tile != pos:
                    now_col = pos % w
                    now_row = pos / w
                    mtable[tile][pos] = math.fabs(now_col - dest_col) + math.fabs(now_row - dest_row)

    return mtable

# @profile
# def main():
#     s = puzzle_state(10)
#     puzzle_state.mtable = [[1,2,3,4,5] for i in xrange(10)]
#     s.mtable = [['asfsadfsaf'] for i in xrange(4)]
#     print puzzle_state.mtable
#     print s.mtable
#     s1 = puzzle_state(4)
#     s1.mtable = [['asfsadfsaf',1,1,1,1,1,1] for i in xrange(40)]
#     print puzzle_state.mtable
#     print s1.mtable


def recur_fib(x):
    if x == 0 or x == 1: return x
    return fib(x-1) + fib(x-2)

def fib(x):
    t = [0, 1]
    for i in xrange(x):
        t.append(t[-1] + t[-2])
    return t[-2]

if __name__ == '__main__':
    #performance test between iteration and recursion
    # t1 = datetime.datetime.now()
    # fib(100000)
    # print 'iteration:  ' + str(datetime.datetime.now() - t1)
    # recur_fib(100000)
    # print 'recursion:  ' + str(datetime.datetime.now() - t1)

    t1 = datetime.datetime.now()
    result = None
    result = idastar(3,2,[5,4,3,2,1,0])
    print 'idastar:  ' + str(datetime.datetime.now() - t1)
    print result

    t1 = datetime.datetime.now()
    result = None
    result = ids(3,2,[5,4,3,2,1,0])
    print 'ids:  ' + str(datetime.datetime.now() - t1)
    print result

    t1 = datetime.datetime.now()
    result = greedy(3,3,[3,5,1,6,8,4,7,0,2])
    print 'greedy:  ' + str(datetime.datetime.now() - t1)
    print result

    t1 = datetime.datetime.now()
    result = astar(2,2,[3,2,1,0])
    print 'astar:  ' + str(datetime.datetime.now() - t1)
    print result

    t1 = datetime.datetime.now()
    result = ucs(2,2,[3,2,1,0])
    print 'ucs:  ' + str(datetime.datetime.now() - t1)
    print result
