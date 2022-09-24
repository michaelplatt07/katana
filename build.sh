#!/bin/sh
nasm -f elf64 ./sample_programs/sample.asm
ld -o ./sample_programs/sample ./sample_programs/sample.o
./sample_programs/sample
