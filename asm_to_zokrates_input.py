#!/usr/bin/python

"""
Translates an .asm file into opcodes and outputs
them in the ZoKrates input JSON format.
"""

import json
import sys

opcodes = {
	'stop': 0x00,
	'add': 0x01,
	'mul': 0x02,
	'sub': 0x03,
	'lt': 0x10,
	'eq': 0x14,
	'sha3': 0x20,
	'calldataload': 0x35,
	'pop': 0x50,
	'jump': 0x56,
	'jumpi': 0x57,
	'push32': 0x7f,
	'dup1': 0x80,
	'dup2': 0x81,
	'dup3': 0x82,
	'swap1': 0x90
}

calldata_size = 32
program_size = 32

def formatNumberAsHexBytes(n):
	return '0x{:08X}'.format(n)

def compile_asm(lines):
	instructions = []
	values = []
	for i, line in enumerate(lines):
		if line.startswith('// values: '):
			if i < len(lines) - 1:
				raise Exception('Calldata values must be specified at the end of the file.')
			calldata = line.split('values: ')[1]
			values = [formatNumberAsHexBytes(int(v)) for v in calldata.split(' ')]
			continue

		line = line.replace('\n', '')
		args = line.split(' ')
		if len(args) == 0:
			raise Exception('Expected opcode, found: ' + line)

		op = args[0]
		if op not in opcodes:
			raise Exception('Unknown opcode: ' + op)

		formatted = formatNumberAsHexBytes(opcodes[op])
		instructions.append(formatted)

		if op == 'push32':
			if len(args) != 2:
				raise Exception('Opcode \"push32\" needs an argument.')
			instructions.append(formatNumberAsHexBytes(int(args[1])))

	return (instructions, values)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage: ' + sys.argv[0] + ' code.asm')
		sys.exit(1)

	fname = sys.argv[1]
	(instructions, values) = compile_asm(open(fname, 'r').readlines())

	if len(instructions) > program_size:
		raise Exception('Programs larger than 32 instructions are not supported.')
	if len(instructions) < program_size:
		instructions.extend((program_size - len(instructions)) * [formatNumberAsHexBytes(opcodes['stop'])])

	if len(values) > calldata_size:
		raise Exception('Calldata larger than 32 values is not supported.')
	if len(values) < calldata_size:
		values.extend((calldata_size - len(values)) * [formatNumberAsHexBytes(0)])

	zkInput = []
	# Memory hash 
	zkInput.append(formatNumberAsHexBytes(0));
	# Stack hash 
	zkInput.append(formatNumberAsHexBytes(0));
	# Instructions
	zkInput.append({"instructions": instructions})
	# Calldata
	zkInput.append({"values": values})

	print(json.dumps(zkInput, indent=4))
