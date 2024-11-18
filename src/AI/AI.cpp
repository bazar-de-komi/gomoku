/*
** EPITECH PROJECT, 2024
** gomoku
** File description:
** AI
*/

#include "src/ai/AI.hpp"
#include "Constants.hpp"

namespace gomoku
{
    AI::AI()
    {
    }


    AI::~AI()
    {
    }

    std::vector<std::pair<int, int>> AI::_generate_possible_moves(const std::vector<std::vector<TableCell>> &board)
    {
        std::vector<std::pair<int, int>> possible_moves;

        for (std::size_t y = 0; y < board.size(); ++y) {
            for (std::size_t x = 0; x < board[y].size(); ++x) {
                if (board[y][x] == TableCell::CELL_EMPTY) {
                    possible_moves.emplace_back(y, x);
                }
            }
        }
        return possible_moves;
    }

    int AI::_simulate_random_game(std::vector<std::vector<TableCell>> board, TableCell current_player)
    {
        while (true) {
            if (_is_terminal(board, TableCell::CELL_AI)) {
                return 1;
            }
            if (_is_terminal(board, TableCell::CELL_PLAYER)) {
                return -1;
            }
            std::vector<std::pair<int, int>> moves = _generate_possible_moves(board);
            if (moves.empty()) {
                return 0;
            }
            auto move = moves[std::rand() % moves.size()];
            board[move.first][move.second] = current_player;
            current_player = (current_player == TableCell::CELL_AI) ? TableCell::CELL_PLAYER : TableCell::CELL_AI;
        }
    }

    bool AI::_check_horizontal(const std::vector<std::vector<TableCell>> &board, const TableCell &player)
    {
        int count = 0;

        for (std::size_t j = 0; j < board.size(); ++j) {
            for (std::size_t i = 0; i < board[j].size(); ++i) {
                if (board[j][i] == player) {
                    count++;
                    if (count == 5) {
                        return true;
                    }
                } else {
                    count = 0;
                }
            }
        }
        return false;
    }

    bool AI::_check_vertical(const std::vector<std::vector<TableCell>> &board, const TableCell &player)
    {
        int rows = board.size();
        int cols = board[0].size();
        int count = 0;

        for (int i = 0; i < rows; ++i) {
            count = 0;
            for (int j = 0; j < cols; ++j) {
                if (board[i][j] == player) {
                    count++;
                    if (count == 5) return true;
                } else {
                    count = 0;
                }
            }
        }
        return false;
    }

    bool AI::_check_diagonal_to_down(const std::vector<std::vector<TableCell>> &board, const TableCell &player)
    {
        std::vector<std::pair<int, int>> cells;
        std::pair<int, int> cell_back_copy;

        for (std::size_t j = 0; j < board.size(); ++j) {
            for (std::size_t i = 0; i < board[j].size(); ++i) {
                if ((i > board[j].size() - 5 && j < 5) ||
                (i < 5 && j > board.size())) {
                    continue;
                }
                if (cells.empty() && board[j][i] == player) {
                    cells.emplace_back(j, i);
                    continue;
                }
                if (i > 0 && j > 0 && !cells.empty()) {
                    cell_back_copy = cells.back();
                    if (cell_back_copy.first == j - 1 && cell_back_copy.second == i - 1) {
                        if (board[j][i] == player) {
                            cells.emplace_back(j, i);
                            continue;
                        } else {
                            cells.clear();
                            continue;
                        }
                    }
                }
                if (cells.size() == 5) {
                    return true;
                }
            }
        }
        return false;
    }

    bool AI::_check_diagonal_to_up(const std::vector<std::vector<TableCell>> &board, const TableCell &player)
    {
        return false;
    }

    bool AI::_is_board_full(const std::vector<std::vector<TableCell>> &board)
    {
        for (const auto &column : board) {
            for (TableCell cell : column) {
                if (cell == TableCell::CELL_EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }

    bool AI::_is_terminal(const std::vector<std::vector<TableCell>> &board, const TableCell &player)
    {
        if (_check_horizontal(board, player)) {
            return true;
        }
        if (_check_vertical(board, player)) {
            return true;
        }
        if (_check_diagonal_to_down(board, player)) {
            return true;
        }
        if (_check_diagonal_to_up(board, player)) {
            return true;
        }
        if (_is_board_full(board)) {
            return true;
        }
        return false;
    }

    std::string AI::play_ai_turn(const std::vector<std::vector<TableCell>> &board)
    {
        std::vector<std::pair<int, int>> possible_ai_moves = _generate_possible_moves(board);
        std::vector<int> scores(possible_ai_moves.size(), 0);
        std::vector<int> simulations(possible_ai_moves.size(), 0);
        int result = 0;
        int best_index = 0;
        double best_ratio = 0;
        double ratio = 0;

        for (size_t j = 0; j < possible_ai_moves.size(); ++j) {
            for (int i = 0; i < MAX_SIMULATIONS; ++i) {
                auto board_copy = board;
                auto move = possible_ai_moves[j];
                board_copy[move.first][move.second] = TableCell::CELL_AI;
                result = _simulate_random_game(board_copy, TableCell::CELL_PLAYER);
                scores[j] += result;
                simulations[j] += 1;
            }
        }
        best_index = 0;
        best_ratio = -1.0;
        for (size_t i = 0; i < possible_ai_moves.size(); ++i) {
            if (simulations[i] == 0) {
                ratio = 0;
            } else {
                ratio = (double)scores[i] / simulations[i];
            }
            if (ratio > best_ratio) {
                best_ratio = ratio;
                best_index = i;
            }
        }
        std::string ai_play = std::to_string(possible_ai_moves[best_index].second);
        ai_play += ",";
        ai_play += std::to_string(possible_ai_moves[best_index].first);
        return ai_play;
    }
}
