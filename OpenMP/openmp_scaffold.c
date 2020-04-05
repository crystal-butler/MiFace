/*
Input: 56000 text files about 500MB each. 
Goal: Check each line in each file for each of 2189 words in a list.

The main work distribution:
MPI:
- Create p processes. 
- Each process will be responsible for NUMFILES/p.
OpenMP:
- Inside each process, we create t threads.
- There are two options:
option 1: Each thread will be responsible for a file.
option 2: All threads will work on a single file to finish it fast.


Compilation:
mpicc -fopenmp -Wall -std=c99 -o progname forCrystal.c

Execution:
mpiexec -n p  progname [arguments]
p is the number of processes you want.

Note: use the highest version of gcc you can find because openmp is embedded within gcc. The higher gcc the more updated openmp.
*/

#include <stdio.h>
#include <stdlib.>
#include <mpi.h>
#include <omp.h>

#define WORDS 2189
#define NUMFILES 56000

/**********************************/
int main(int argc, char *argv[]){

  int numprocs; /* num of processes */
  int rank; /* rank of the calling process from 0 to num processes -1 */
  int numfiles; /* number of files to be processed by each process */
  FILE ** files; /* Array of pointers to files opened by each process */
  int i;

  /* Step 0: MPI part: setting the stage */
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  
  numfiles = NUMFILES/numprocs; // You may want to take care of the corner case if there is a remainder.
  files = (FILE **)malloc(numfiles * sizeof(FILE *));
 
 /* At that point, each process knows its rank. So you need to assign files to processes based on the rank */
 
 
 
 /* Step 1: Open file files */
 /* Each process opens all the files or subset depending on any restrictions the system is imposing for number of files opened by a process.*/
 for( i = 0; i < numfiles; i++){
  /* open a file and put the file handle in files[]; */
 }	 
 /* Now all the files are open and ready to be processed */
 
 
 
 /* Step 2: OpenMP part: process each file */
 /* Pick one of the two options but not both. */
 //option 1:
 #pragma omp parallel for
 for(i = 0; i < numfiles; i++){
	 /* Here you put the work done by each thread. In this option, each thread is respnsible for one or more files. 
	 The runtime will decide since I didn't specifiy the number of threads. You don't need to worry about work how many files per thread.
	 */
 }
 
 //option 2:
 /* If you can read the whole file into a buffer it will be faster.
     IF not, read the maximum you can read in buffer[]. 
	 When done processing it, overwrite it with the new part of the file. */
 for(i = 0; i < numfiles; i++){
 /* Assume we have the whole file, or part of it, in buffer[] */
 /*
 #pragma omp parallel for
    for( int j = 0; j < numwords in buffer; j++)
	{
		read word
        compare that word with the list of words in the list		
	}
 
  */
 }
 
 
 /* Any IO you want */
 
 /* Don't forget to close the files */
 
  MPI_Finalize();	
}
/**********************************/