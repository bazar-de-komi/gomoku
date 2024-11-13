/*
** EPITECH PROJECT, 2024
** gomoku
** File description:
** Parser.cpp
*/

#include "src/parser/Parser.hpp"
#include "Constants.hpp"

namespace gomoku
{

    Parser::Parser() {}

    Parser::Parser(int argc, char **argv) : _argc(argc), _argv(argv) {}


    Parser::~Parser() {}

    int Parser::mainloop()
    {
        return SUCCESS;
    }
}
