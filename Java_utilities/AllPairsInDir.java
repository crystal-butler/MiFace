// author: Crystal Butler
// 06/02/2015

/* create all combinations of 2, no repetition, for up to 40
   word labels in a file for all files in a directory. May
   have problems running on directories not in same parent directory
   as program */

import java.io.*;
import java.util.*;

public class AllPairsInDir
{
	public static void main(String args[]) throws IOException
	{
		// get the directory path from standard input
		Scanner filePath = new Scanner(System.in);
		System.out.println("Input directory: ");
		System.out.flush();
		String dirName = filePath.nextLine();
		
		// create an array of all the file names in the directory
		File[] inputFiles = new File(dirName).listFiles();
		
		// declare an output file for processing results
		FileWriter outputFile = null;		
		
		// Create & initialize array for all word labels in a file
		String [] labelSet = new String [100];
		// Arrays.fill (labelSet, "null");

		// process all the files in the directory
		for (File file : inputFiles)
		{

			try
			{
				// open a file and create a corresponding output file
				String fileName = file.getName();
				File inputFile = new File (dirName + "/" + fileName);
				Scanner label = new Scanner (inputFile);
				outputFile = new FileWriter(inputFile + ".out.txt");

				// load all word labels in a file into an array, after initializing it to nulls
				Arrays.fill (labelSet, "null");
				int a = 0;
				while (label.hasNext())
				{
					labelSet[a]=label.next();
					a++;
				}

				// create the ouput file of all pairs, no repetition
				int i = 0;
				for (i=0; i<labelSet.length; i++)
				{
					if (!labelSet[i].equals("null"))
					{
						for (int j=(i+1); j<labelSet.length; j++)
						{
							if (!labelSet[j].equals("null"))
							{
								outputFile.write(labelSet[i] + " " + labelSet[j] + "\n");
							}
						}
					}
				}
				
				label.close();
			}

			catch (FileNotFoundException e) 
			{
				e.printStackTrace();
			}

			finally 
			{
				if (outputFile != null)
				{
					outputFile.close();
				}
			}

		}

	}

}