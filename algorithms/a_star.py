import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# Posição (linha, coluna) de cada peça no estado objetivo
GOAL_POSITIONS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan (ignora o espaço vazio)."""
        total = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(i, 3)
            goal_row, goal_col = GOAL_POSITIONS[tile]
            total += abs(row - goal_row) + abs(col - goal_col)
        return total

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        tie = count()  # desempate entre nós com o mesmo f
        frontier = [(self.heuristic(initial), next(tie), initial)]
        best_cost = {initial.tiles: initial.cost}

        while frontier:
            _, _, node = heapq.heappop(frontier)

            # Ignora entradas antigas (já existe caminho melhor)
            if node.cost > best_cost.get(node.tiles, float("inf")):
                continue

            if node.is_goal:
                result.solution = node
                result.depth = node.cost
                return result

            result.nodes_expanded += 1

            for child in node.neighbors():
                result.nodes_generated += 1
                if child.cost < best_cost.get(child.tiles, float("inf")):
                    best_cost[child.tiles] = child.cost
                    f = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (f, next(tie), child))

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
