SRC=$(wildcard *.c)  
EXE=out

CXXFLAGS+=-Wall -Wextra -MMD -g -O2
LDFLAGS=-lncurses

OBJ=$(addprefix build/,$(SRC:.c=.o))
DEP=$(addprefix build/,$(SRC:.c=.d))

all: $(OBJ)
	gcc -o $(EXE) $^ $(LDFLAGS)

build/%.o: %.c
	@mkdir -p build
	gcc $(CXXFLAGS) -o $@ -c $<

clean:
	rm -rf build core

-include $(DEP)
