#!/bin/sh
nasm -f elf64 sample_programs/reference.asm
ld -o sample_programs/reference sample_programs/reference.o
./sample_programs/reference
