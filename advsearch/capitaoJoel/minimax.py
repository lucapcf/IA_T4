import random
from typing import Tuple, Callable



def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    _, best_action = MAX(state, eval_func, max_depth, float('-inf'), float('inf'))
    return best_action
    
def MAX(state, eval_func: Callable, depth: int, alpha: float, beta: float) -> Tuple[float, Tuple[int, int]]:
    if state.is_terminal() or depth == 0:
        util = eval_func(state, state.player)
        return util, None
    
    v = float('-inf')
    best_action = None
    for action in state.legal_moves():
        successor = state.next_state(action)
        v2, _ = MIN(successor, eval_func, depth - 1, alpha, beta)
        if v2 > v:
            v = v2
            best_action = action
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v, best_action


def MIN(state, eval_func: Callable, depth: int, alpha: float, beta: float) -> Tuple[float, Tuple[int, int]]:
    if state.is_terminal() or depth == 0:
        return eval_func(state, state.player), None
    
    v = float('inf')
    best_action = None
    for action in state.legal_moves():
        successor = state.next_state(action)
        v2, _ = MAX(successor, eval_func, depth - 1, alpha, beta)
        if v2 < v:
            v = v2
            best_action = action
        beta = min(beta, v)
        if alpha >= beta:
            break
    return v, best_action
