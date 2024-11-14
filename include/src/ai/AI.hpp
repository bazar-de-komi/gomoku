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
    };
}
