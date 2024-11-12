##
## EPITECH PROJECT, 2024
## B-AIA-500-PAR-5-1-gomoku-eric1.xu
## File description:
## Makefile
##

CC	=	g++

RM	=	rm -rf

SRC	=	./Main.cpp \
\
		./src/Ia.cpp	\
		./src/Parser.cpp	\
\

OBJ	=	$(SRC:.cpp=.o)

CXXFLAGS	=	-Wall -Wextra

CPPFLAGS	=	-iquote ./include

NAME	=	pbrain-gomoku-ai

all: 		$(NAME)

$(NAME):		$(OBJ)
	$(CC) $(OBJ) -o $(NAME) $(LDFLAGS) $(LDLIBS)


clean:
	$(RM) $(OBJ)


fclean: clean
	$(RM) $(NAME)

re:	fclean all

debug:	CFLAGS += -g3
debug:	clean all

.PHONY:	all clean fclean re debug
