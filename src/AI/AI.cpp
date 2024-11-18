/*
** EPITECH PROJECT, 2024
** gomoku
** File description:
** AI
*/

#include "src/ai/AI.hpp"

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
        return possible_moves;
    }
    int AI::_simulate_random_game(std::vector<std::vector<TableCell>> board, TableCell current_player)
    {
        return 0;
    }
    bool AI::_check_horizontal(const std::vector<std::vector<TableCell>> &board)
    {
        return false;
    }
    bool AI::_check_vertical(const std::vector<std::vector<TableCell>> &board)
    {
        return false;
    }
    bool AI::_check_diagonal_to_down(const std::vector<std::vector<TableCell>> &board)
    {
        return false;
    }
    bool AI::_check_diagonal_to_up(const std::vector<std::vector<TableCell>> &board)
    {
        return false;
    }
    bool AI::_is_terminal(const std::vector<std::vector<TableCell>> &board)
    {
        return false;
    }

    std::string AI::play_ai_turn(const std::vector<std::vector<TableCell>> &board)
    {
        return "";
    }
}
