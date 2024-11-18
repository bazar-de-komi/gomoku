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
#include "src/ai/AI.hpp"

namespace gomoku
{
    class Parser {
        public:
        Parser();
        Parser(int argc, char **argv);
        Parser(int argc, char **argv, AI &ai);
        ~Parser();

        int mainloop();
        private:
        AI &_ai;
        std::vector<std::string> get_commands();
        std::vector<std::vector<TableCell>> _map;
        int _argc = 0;
        int _board_size = 0;
        char **_argv = nullptr;
    };
}

