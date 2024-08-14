import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Máscara de avaliação posicional
POSITION_MASK = [
    [120, -20,  20,   5,   5,  20, -20, 120],
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
    [ 20,  -5,  15,   3,   3,  15,  -5,  20],
    [  5,  -5,   3,   3,   3,   3,  -5,   5],
    [  5,  -5,   3,   3,   3,   3,  -5,   5],
    [ 20,  -5,  15,   3,   3,  15,  -5,  20],
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
    [120, -20,  20,   5,   5,  20, -20, 120]
]

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    max_depth = 4  # Ajuste a profundidade conforme necessário para garantir que os movimentos sejam calculados dentro de 5 segundos
    return minimax_move(state, max_depth, evaluate_custom)

def evaluate_custom(state: GameState, player: str) -> float:
    """
    Avalia um estado do Othello do ponto de vista do jogador dado.
    Se o estado for terminal, retorna sua utilidade.
    Se não for terminal, retorna uma estimativa de seu valor com base em uma heurística personalizada.
    :param state: estado a ser avaliado (instância de GameState)
    :param player: jogador para o qual o estado está sendo avaliado (B ou W)
    """
    if state.is_terminal():
        winner = state.winner()  # Assuming the method is called 'winner()'
        if winner == player:
            return 1.0
        elif winner is None:  # It's a draw
            return 0.0
        else:
            return -1.0

    opponent = 'B' if player == 'W' else 'W'
    board = state.get_board()

    # 1. Diferença de peças ponderada
    player_count = board.num_pieces(player)
    opponent_count = board.num_pieces(opponent)
    piece_diff = (player_count - opponent_count) / (player_count + opponent_count)

    # 2. Avaliação posicional
    position_score = 0
    for row in range(8):
        for col in range(8):
            if board.get_piece(row, col) == player:
                position_score += POSITION_MASK[row][col]
            elif board.get_piece(row, col) == opponent:
                position_score -= POSITION_MASK[row][col]

    # 3. Mobilidade (número de movimentos legais)
    player_mobility = len(state.legal_moves())
    state.player = opponent
    opponent_mobility = len(state.legal_moves())
    state.player = player
    mobility = (player_mobility - opponent_mobility) / (player_mobility + opponent_mobility + 1)

    # 4. Estabilidade dos cantos
    corners = [(0,0), (0,7), (7,0), (7,7)]
    player_corners = sum(1 for corner in corners if board.get_piece(corner[0], corner[1]) == player)
    opponent_corners = sum(1 for corner in corners if board.get_piece(corner[0], corner[1]) == opponent)
    corner_stability = (player_corners - opponent_corners) / 4

    # 5. Paridade (vantagem de fazer o último movimento)
    parity = 1 if (64 - player_count - opponent_count) % 2 == 0 else -1

    # Pesos para cada componente da heurística
    w_piece_diff = 0.25
    w_position = 0.35
    w_mobility = 0.15
    w_corner = 0.2
    w_parity = 0.05

    # Combinação ponderada das heurísticas
    evaluation = (
        w_piece_diff * piece_diff +
        w_position * position_score / 100 +  # Normalizado para estar aproximadamente entre -1 e 1
        w_mobility * mobility +
        w_corner * corner_stability +
        w_parity * parity
    )

    return evaluation