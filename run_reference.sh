#!/bin/sh
nasm -f elf64 reference.asm
ld -o reference reference.o
./reference
echo $?
