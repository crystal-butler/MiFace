// author: Crystal Butler
//06/02/2015

import java.io.*;
import java.util.*;
import java.util.IntSummaryStatistics;
import java.util.Scanner;

public class LabelStats
{
	public static void main(String args[]) throws IOException
	{
		// read in a Directory name: must contain only files with int scores
		Scanner filePath = new Scanner (System.in);
		System.out.println("Input directory: ");
		System.out.flush();
		String dirName = filePath.nextLine();
		File[] inputFiles = new File(dirName).listFiles();
		FileWriter outputFile = null;
		int score = 0;

		// run stats on all files in the directory
		for (File file : inputFiles)
		{
			// Java 8+ only: aggregates input for stats
			// If not reinitialized, will continue to aggregate over all files
			IntSummaryStatistics labelStats = new IntSummaryStatistics();
			try
			{
				String fileName = file.getName();

				// for Mac, if show hidden files is turned on
				if (fileName.equals(".DS_Store"))
				{
					continue;
				}
				//System.out.println (fileName);

				// open a file in the directory for processing
				File inputFile = new File(dirName + "/" + fileName);
				//System.out.println (inputFile);
				Scanner leskScores = new Scanner (inputFile);

				// aggregate int scores to generate stats
				while (leskScores.hasNextInt())
				{
					//System.out.println(leskScores.next());
					score = leskScores.nextInt();
					labelStats.accept(score);
				}

				// calculate z-score based on all-adjectives mean and standard deviation
				double zVal = (labelStats.getAverage()-6.26)/(9.45/(Math.sqrt(labelStats.getCount())));
				
				String zValString = String.valueOf(zVal);
				String countString = String.valueOf(labelStats.getCount());
				String avgString = String.valueOf(labelStats.getAverage());
				String minString = String.valueOf(labelStats.getMin());
				String maxString = String.valueOf(labelStats.getMax());

				String count = new String("Count: " + countString);
				String avg = new String("Average: " + avgString);
				String min = new String("Minimum: " + minString);
				String max = new String("Maximum: " + maxString);
				String zScore = new String("z-score: " + zValString);
				
				/* System.out.println (count);
				System.out.println (avg);
				System.out.println (min);
				System.out.println (max);
				System.out.println (zScore); */

				// save the stats to an output file
				outputFile = new FileWriter(inputFile + ".stats.txt");
				outputFile.write("Count: " + count + "\n");
				outputFile.write("Average: " + avg + "\n");
				outputFile.write("Minimum: " + min + "\n");
				outputFile.write("Maximum: " + max + "\n");
				outputFile.write("z-score: " + zValString);

				// close the file reader (scanner)
				leskScores.close();
			}
			catch (FileNotFoundException e) 
			{
				e.printStackTrace();
			}
			finally 
			{
				if (outputFile != null)
				{
					// close the output file
					outputFile.close();
				}
			} 
		}
	}
}
