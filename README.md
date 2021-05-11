TinyZKEVM
---------

This is an under development very small proof of concept implementation of a
subset of the EVM inside a SNARK, using [ZoKrates](https://zokrates.github.io/).
For now there is no state, no account, no calls, and the memory, stack and
program are very small.


Compiling
=========

In order to compile TinyZKEVM you need a
[custom ZoKrates](https://github.com/leonardoalt/ZoKrates/tree/zkevm_patch), then:

```
$ zokrates -i src/vm.zok
```

In order to compute an execution witness, the VM takes 4 arguments:

1. Hash of the memory at the end of execution (not used at the moment).
2. Hash of the stack at the end of execution (not used at the moment).
3. The TinyZKEVM bytecode.
4. The private calldata.

The easiest way to compute a witness and read the memory and stack outputs is
by creating a JSON input file:

```
[
	"0x00000000",
	"0x00000000",
	{
		"instructions": ["0x0000007f", "0x0000000a", "0x0000007f", "0x00000004", "0x00000001", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000"]
	},
	{
		"values": ["0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000"]
	}
]
```

The size of `instructions` and `values` must match the data structures in `src/data.zok`.

Then run:

```
$ cat input.json | zokrates compute-witness --stdin --abi --verbose
```

TODOs
=====

A lot of stuff.
