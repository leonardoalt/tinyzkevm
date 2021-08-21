#!/usr/bin/bash

# Usage: ./run_test.sh [--no-witness] [-u|--update] input.asm

localExit()
{
	rm $tmpfile

	if [[ -f "witness" ]]
	then
		rm "witness"
	fi

	exit $1
}

COMPUTE_WITNESS=1
WITNESS_VERBOSE=0
UPDATE_ALL=0

for arg in "$@"
do
	case $arg in
		--no-witness)
		COMPUTE_WITNESS=0
		shift
		;;
		--witness-verbose)
		WITNESS_VERBOSE=1
		shift
		;;
		-u|--update)
		UPDATE_ALL=1
		shift
		;;
	esac
done

tmpfile=$(mktemp ./$1.tmp.XXXXXX.json)

echo "Translating $1 to ZoKrates JSON input format..."

# Translate asm to json input format.
./asm_to_zokrates_input.py $1 > $tmpfile

expected="$1.json"
while ! cmp -s $expected $tmpfile ;
do
	echo "$(cmp -s $expected $tmpfile)"
	echo "Expected and compile JSON input files differ:"
	echo "Expected:"
	cat $expected
	echo "But got:"
	cat $tmpfile
	echo "What do you wanna do? (u)pdate, (i)gnore, (q)uit"

	if [[ UPDATE_ALL -eq 1 ]]
	then
		cp $tmpfile $expected
		continue
	fi

	read -rsn1 cmd

	if [[ "$cmd" == "u" ]]
	then
		cp $tmpfile $expected
	elif [[ $cmd == "i" ]]
	then
		break
	elif [[ $cmd == "q" ]]
	then
		localExit 1
	else
		echo "Unknown command, ignoring."
		break
	fi
done

if [[ COMPUTE_WITNESS -eq 1 ]]
then
	echo "Computing witness for $1..."

	ZK_EXTRA=""
	if [[ WITNESS_VERBOSE -eq 1 ]]
	then
		ZK_EXTRA=" --verbose"
	fi
	cat $tmpfile | zokrates compute-witness --stdin --abi $ZK_EXTRA

	if [ $? -eq 0 ]; then
		echo "OK"
	else
		echo "FAILED"
		localExit 1
	fi
else
	echo "Skipping witness computation."
fi

localExit 0
