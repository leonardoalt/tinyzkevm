#!/usr/bin/sh

cat "tests/$1.json" | zokrates compute-witness --stdin --abi --verbose
