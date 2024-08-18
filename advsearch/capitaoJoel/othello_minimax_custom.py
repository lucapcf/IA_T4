import random
from typing import Tuple, Dict
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Template de avaliação para valorizar posições estratégicas no tabuleiro
EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

# Cache para memorização de estados já avaliados
evaluation_cache: Dict[str, float] = {}

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    max_depth = 5
    return minimax_move(state, max_depth, evaluate_custom)

def evaluate_custom(state, player:str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on your custom heuristic
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    # Memorização para evitar reavaliações
    state_str = str(state.board) + player
    if state_str in evaluation_cache:
        return evaluation_cache[state_str]
    
    opponent = 'B' if player == 'W' else 'W'
    
    # Avaliação da posição no tabuleiro baseada no template
    player_score = 0
    opponent_score = 0
    
    for row in range(8):
        for col in range(8):
            piece = state.board.get_piece(row, col)
            if piece == player:
                player_score += EVAL_TEMPLATE[row][col]
            elif piece == opponent:
                opponent_score += EVAL_TEMPLATE[row][col]

    positional_score = player_score - opponent_score

    # Avaliação baseada no controle de cantos
    player_corners = count_corners(state, player)
    opponent_corners = count_corners(state, opponent)
    corner_score = 100 * (player_corners - opponent_corners)

    # Avaliação baseada no número total de peças
    player_pieces = state.board.num_pieces(player)
    opponent_pieces = state.board.num_pieces(opponent)
    piece_score = player_pieces - opponent_pieces

    # Avaliação baseada na mobilidade
    player_moves = len(state.board.legal_moves(player))
    opponent_moves = len(state.board.legal_moves(opponent))
    mobility_score = 10 * (player_moves - opponent_moves)

    # Avaliação baseada na estabilidade
    player_stability = count_stable_pieces(state, player)
    opponent_stability = count_stable_pieces(state, opponent)
    stability_score = 50 * (player_stability - opponent_stability)

    # Avaliação baseada na paridade
    parity_score = 0
    if len(state.board.legal_moves(player)) % 2 == 0:
        parity_score = 5  # Preferência por posições onde o número de jogadas restantes é par

    # Combinação das heurísticas com pesos ajustados
    score = positional_score + corner_score + 0.1 * piece_score + mobility_score + stability_score + parity_score
    evaluation_cache[state_str] = score
    return score

def count_corners(state: GameState, player: str) -> int:
    """
    Conta o número de cantos controlados pelo jogador.
    :param state: estado a ser avaliado (instância de GameState)
    :param player: jogador para avaliar o estado (B ou W)
    :return: número de cantos controlados pelo jogador
    """
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    count = 0
    for x, y in corners:
        if state.board.get_piece(x, y) == player:
            count += 1
    return count

def count_stable_pieces(state: GameState, player: str) -> int:
    """
    Conta o número de peças estáveis do jogador, ou seja, peças que não podem ser capturadas.
    :param state: estado a ser avaliado (instância de GameState)
    :param player: jogador para avaliar o estado (B ou W)
    :return: número de peças estáveis do jogador
    """
    stable_count = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    for row in range(8):
        for col in range(8):
            if state.board.get_piece(row, col) == player and is_stable(state, player, row, col, directions):
                stable_count += 1
                
    return stable_count

def is_stable(state: GameState, player: str, row: int, col: int, directions: list) -> bool:
    """
    Verifica se uma peça é estável, ou seja, se não pode ser capturada por nenhum movimento subsequente.
    :param state: estado a ser avaliado (instância de GameState)
    :param player: jogador para avaliar o estado (B ou W)
    :param row: linha da peça
    :param col: coluna da peça
    :param directions: direções a serem verificadas para estabilidade
    :return: True se a peça é estável, False caso contrário
    """
    for dx, dy in directions:
        x, y = row + dx, col + dy
        while 0 <= x < 8 and 0 <= y < 8:
            if state.board.get_piece(x, y) != player:
                break
            x += dx
            y += dy
        else:
            return True
    return False
