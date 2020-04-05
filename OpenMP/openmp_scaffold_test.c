/*
Input: 56000 text files about 500MB each. 
Goal: Check each line in each file for each of 2189 words in a list.

The main work distribution for 8 files: (one process + eight threads)


Compilation:
gcc -fopenmp -Wall -std=c99 -o progname forCrytal.c


Note: use the highest version of gcc you can find because openmp is embedded within gcc. The higher gcc the more updated openmp.
*/

#include <stdio.h>
#include <stdlib.>
#include <string.h>
#include <omp.h>

#define WORDS 2189
#define NUMFILES 8
#define MAXCHAR 100  //maximum number of characters for a filename or a word

/**********************************/
int main(int argc, char *argv[]){


  FILE ** files; /* Array of pointers to files opened by each process */
  int numfiles = 8;  /* number of files to be processed for this version */
  int i, j; //loop indices
  char filenames[8][MAXCHAR];
  char words[WORDS][MAXCHAR]; 
  char aword[MAXCHAR]; // a word read from the file

  /* TODO:  load file names into the array filenames[][] */

  files = (FILE **)malloc(numfiles * sizeof(FILE *));
  
  // open the files
  for (i = 0; i < numfiles; i++)
	  if(!(files[i] = fopen(filenames[i],"r+t"))
	  {
		  printf("Cannot open file %s\n", filenames[i]);
		  exit(0);
	  }
  
 
 /* TODO: load words into words[][]*/
 
 // create number of threads = number of files and each thread will take care of one loop iteration
 #pragma omp parallel for num_threads(num_files)
 for(i = 0; i < num files; i++)
 {
	 //read word from the file compare with a list of words
	 while( fgets(aword, MAXCHAR, files[i]) != NULL)
		 for(j = 0; j < WORDS; j++)
			 if(!strcmp(aword, words[j]))
			 {
				 /* a match is found, do something */
			 }
 }
 
 
 
 /* Any IO you want */
 
 
 //close the files
 for(i = 0; i < numfiles; i++)
	 fclose(files[i]);
 
 exit 0;
}
/**********************************/