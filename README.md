TinyZKEVM
---------

This is an under development very small proof of concept implementation of a
subset of the EVM inside a SNARK, using [ZoKrates](https://zokrates.github.io/).
For now there is no state, no account, no calls, and the memory, stack and
program are very small.


Compiling
=========

In order to compile TinyZKEVM you need a version of ZoKrates that has the
`--isolate-branches` compilation feature, then:

```
$ make
```

Running
=======

The VM takes 4 arguments for execution witness computation:

1. Hash of the memory at the end of execution (not used at the moment).
2. Hash of the stack at the end of execution (not used at the moment).
3. The TinyZKEVM bytecode.
4. The private calldata.

You can run tiny EVM programs written in assembly using EVM mnemonics.
The same execution file can also take values for the calldata.

The following `.asm` execution file defines a program that loads the first byte
of calldata, `2` in this case, duplicates it on the stack, pops the top of
the stack and leaves.

```
push32 0
calldataload
dup1
pop
stop
// values: 2
```

The instructions must be given one per line, without empty lines.
Calldata may be given at exactly the last line as separate bytes after `// values: `.

This format only exists to make our life easier, since ZoKrates uses a
[JSON ABI input format](https://zokrates.github.io/toolbox/abi.html).
The script `asm_to_zokrates_input.py` can be used to translate the TinyEVM's execution
format described above to ZoKrates' format.

Please check the `tests` directory to see different execution examples and the
mentioned JSON format.

The script `run_test.sh` can be used directly on an execution `.asm` file.
It invokes the translation script to create the JSON input, and then calls
ZoKrates `compute witness` command.

If you want to run all tests, just call `./run_all.sh` or `make test` if you haven't
compiled the VM yet.

By default the test will not show you the VM's state at the end of the execution,
only whether it succeeded.
If you want to see the post state, run

```
$ ./run_test.sh --witness-verbose program.asm
```

The `--witness-verbose` flag triggers the test script to call ZoKrates witness computation
with its `--verbose` flag, which prints the intermediate representation of the circuit
and the state at the end of execution.


TODOs
=====

A lot of stuff.
