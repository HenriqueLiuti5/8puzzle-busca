import pytest

from puzzle.state import State, GOAL_STATE
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar

GOAL = State(GOAL_STATE)
EASY = State((1, 2, 3, 4, 5, 6, 7, 0, 8))      # 1 movimento
MEDIUM = State((1, 2, 3, 0, 4, 6, 7, 5, 8))    # 3 movimentos
HARD = State((8, 6, 7, 2, 5, 4, 3, 0, 1))      # 31 movimentos
UNSOLVABLE = State((1, 2, 3, 4, 5, 6, 8, 7, 0))


def apply(state, actions):
    for a in actions:
        state = next(c for c in state.neighbors() if c.action == a)
    return state


def test_neighbors():
    assert len(GOAL.neighbors()) == 2
    assert len(State((1, 2, 3, 4, 0, 5, 6, 7, 8)).neighbors()) == 4


def test_path_and_actions():
    child = EASY.neighbors()[0]
    assert child.path() == [EASY, child]
    assert child.actions() == [child.action]
    assert EASY.actions() == []


@pytest.mark.parametrize("algo", [BFS(), DFS(), AStar()])
@pytest.mark.parametrize("initial", [GOAL, EASY, MEDIUM, HARD])
def test_finds_valid_solution(algo, initial):
    r = algo.search(initial)
    assert r.found
    assert apply(initial, r.actions).is_goal
    assert r.depth == r.path_cost == len(r.actions)


@pytest.mark.parametrize("algo", [BFS(), AStar()])
def test_optimal(algo):
    assert algo.search(EASY).depth == 1
    assert algo.search(MEDIUM).depth == 3
    assert algo.search(HARD).depth == 31


def test_heuristic():
    assert AStar().heuristic(GOAL) == 0
    assert AStar().heuristic(EASY) == 1


def test_unsolvable():
    assert not BFS().search(UNSOLVABLE).found
    assert not DFS(depth_limit=8).search(UNSOLVABLE).found
