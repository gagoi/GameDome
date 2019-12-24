SRC=$(wildcard *.cpp)  
EXE=out

CXXFLAGS+=-Wall -Wextra -MMD -g -O2
LDFLAGS=-lncurses

OBJ=$(addprefix build/,$(SRC:.cpp=.o))
DEP=$(addprefix build/,$(SRC:.cpp=.d))

all: $(OBJ)
	gcc -o $(EXE) $^ $(LDFLAGS)

build/%.o: %.cpp
	@mkdir -p build
	gcc $(CXXFLAGS) -o $@ -c $<

clean:
	rm -rf build core

-include $(DEP)
