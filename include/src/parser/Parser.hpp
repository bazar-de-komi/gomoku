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
    class Parser {
        public:
        Parser();
        Parser(int argc, char **argv);
        ~Parser();

        int mainloop();
        private:
        int _argc = 0;
        char **_argv = nullptr;
    };
}

