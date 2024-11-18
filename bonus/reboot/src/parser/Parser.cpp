/*
** EPITECH PROJECT, 2024
** gomoku
** File description:
** Parser.cpp
*/

#include "src/parser/Parser.hpp"
#include "Constants.hpp"
#include "src/ai/AI.hpp"

namespace gomoku
{

    Parser::Parser()
    {
        _ai = AI();
    }

    Parser::Parser(int argc, char **argv) : _argc(argc), _argv(argv)
    {
        _ai = AI();
    }

    Parser::Parser(int argc, char **argv, AI &ai) : _argc(argc), _argv(argv), _ai(ai) {}

    Parser::~Parser() {}

    int Parser::mainloop()
    {
        return SUCCESS;
    }
}
