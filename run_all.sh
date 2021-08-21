#!/usr/bin/bash

for t in ./newTests/*.asm
do
	./run_test.sh $t
	echo ""
done
