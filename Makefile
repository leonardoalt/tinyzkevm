all: compile

compile:
	zokrates compile --isolate-branches -i src/vm.zok

test: compile
	./run_all.sh
