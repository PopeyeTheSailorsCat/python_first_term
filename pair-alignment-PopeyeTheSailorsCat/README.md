#Program structure
##The program consists of two modules:
 * main 
    * implements the program interface
    * contains a function for calculating the Hamming distance
 * NV_alignment  
    * implements the logic of the Needleman–Wunsch algorithm
    * implements the functions required for the algorithm to work
    * if you don't need an interface, you can access this module directly
and use align to perform sequence alignment
    
 There is also a directory with tests tests
  * contains two similar files with tests, one uses unittest
, the other uses regular assert