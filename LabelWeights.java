// author: Crystal Butler
//06/09/2015

import java.io.*;
import java.util.*;
import java.util.IntSummaryStatistics;
import java.util.Scanner;

public class LabelWeights
{
	public static void main(String args[]) throws IOException
	{
		// read in a Directory name: must contain only files with int scores
		Scanner filePath = new Scanner (System.in);
		System.out.println("Input directory: ");
		System.out.flush();
		String dirName = filePath.nextLine();
		File[] inputFiles = new File(dirName).listFiles();
		//FileWriter outputFile = null;
		String label;
		String tempLabel;
		String weightString;
		double weight = 0.0;
		double weightTotal = 0.0;

		// get label weights for all files in a directory
		for (File file : inputFiles)
		{

			try
			{

				String fileName = file.getName();

				// for Mac, if show hidden files is turned on
				if (fileName.equals(".DS_Store"))
				{
					continue;
				}

				// open a file in the directory for processing
				File inputFile = new File(dirName + "/" + fileName);
					System.out.println(inputFile);
				Writer outputFile = new FileWriter(inputFile + ".weights.txt");
				//outputFile.write("test output!\n");//(tempLabel + "\t" + weight + "\n");
				Scanner labelWeights = new Scanner (inputFile);
				
				label = labelWeights.next();
					System.out.println(label);
				while (labelWeights.hasNext())
				{
					tempLabel = label;
					while (label.equals(tempLabel))
					{
						weightString = labelWeights.next();
						weight = Double.parseDouble(weightString);
						weightTotal += weight;
						if(labelWeights.hasNext())
						{
							label = labelWeights.next();
						} else {
							break;
						}				
					}
					outputFile.write(String.format("%s\t%.4f\n", tempLabel, weightTotal));
					weight = 0.0;
					weightTotal = 0.0;	
				}			

				outputFile.close();
				// close the file reader (scanner)
				labelWeights.close();
			}

			catch (FileNotFoundException e) 
			{
				e.printStackTrace();
			}

		}

	}

}
