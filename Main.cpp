/*
** EPITECH PROJECT, 2024
** B-AIA-500-PAR-5-1-gomoku-eric1.xu
** File description:
** main.cpp
*/

#include "Constants.hpp"
#include "src/parser/Parser.hpp"

int main(int argc, char **argv)
{
    gomoku::Parser pars = gomoku::Parser(argc, argv);
    return pars.mainloop();
}
