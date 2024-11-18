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
                if (board[y][x] == TableCell::EMPTY) {
                    possible_moves.emplace_back(y, x);
                }
            }
        }
        return possible_moves;
    }

    int AI::_simulate_random_game(std::vector<std::vector<TableCell>> board, TableCell current_player)
    {
        while (true) {
            if (_is_terminal(board, TableCell::AI)) {
                return 1;
            }
            if (_is_terminal(board, TableCell::PLAYER)) {
                return -1;
            }
            std::vector<std::pair<int, int>> moves = _generate_possible_moves(board);
            if (moves.empty()) {
                return 0;
            }
            auto move = moves[std::rand() % moves.size()];
            board[move.first][move.second] = current_player;
            current_player = (current_player == TableCell::AI) ? TableCell::PLAYER : TableCell::AI;
        }
    }

    bool AI::_check_horizontal(const std::vector<std::vector<TableCell>> &board, TableCell player)
    {
        return false;
    }

    bool AI::_check_vertical(const std::vector<std::vector<TableCell>> &board, TableCell player)
    {
        return false;
    }

    bool AI::_check_diagonal_to_down(const std::vector<std::vector<TableCell>> &board, TableCell player)
    {
        return false;
    }

    bool AI::_check_diagonal_to_up(const std::vector<std::vector<TableCell>> &board, TableCell player)
    {
        return false;
    }

    bool AI::_is_terminal(const std::vector<std::vector<TableCell>> &board, TableCell player)
    {
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
                board_copy[move.first][move.second] = TableCell::AI;
                result = _simulate_random_game(board_copy, TableCell::PLAYER);
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
