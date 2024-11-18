/*
** EPITECH PROJECT, 2024
** gomoku
** File description:
** AI
*/

#pragma once

    #include <vector>
    #include <string>
    #include "src/Data.hpp"

namespace gomoku
{
    class AI {
        public:
            AI();
            ~AI();

            std::string play_ai_turn(const std::vector<std::vector<TableCell>> &);
        private:
            std::vector<std::pair<int, int>> _generate_possible_moves(const std::vector<std::vector<TableCell>> &);
            int _simulate_random_game(std::vector<std::vector<TableCell>>, TableCell);
            bool _check_horizontal(const std::vector<std::vector<TableCell>> &, const TableCell &);
            bool _check_vertical(const std::vector<std::vector<TableCell>> &, const TableCell &);
            bool _check_diagonal_to_down(const std::vector<std::vector<TableCell>> &, const TableCell &);
            bool _check_diagonal_to_up(const std::vector<std::vector<TableCell>> &, const TableCell &);
            bool _is_board_full(const std::vector<std::vector<TableCell>> &);
            bool _is_terminal(const std::vector<std::vector<TableCell>> &, const TableCell &);
    };
}
