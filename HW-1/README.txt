Construct a Pyhton 3 program to simulate a virtual machine having
1)Memory
  32-bit address space
  8-bit cell
2)Register File
  32 32-bit registers, with 2 read ports and 1 write port

using following test bench
// Add the number in memory address 0 and 1 to address 3
Load r1, #0
Load r2, #1
Add r3, r1, r2
Store r3, #3
