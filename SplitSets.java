/* 05/05/2016 Crystal Butler
 * This class takes as input a text file with lines in the form of 'number,label' as
 * output from the results of an expression labeling study. The number is the image
 * number, and the label is one of a set of words assigned to the image with a particular number.
 */

import java.io.*;
import java.util.*;

public class SplitSets
{
	public static void main(String args[]) throws IOException
	{
		Scanner filePath = new Scanner (System.in);
		System.out.println("Input filename: ");
		System.out.flush();
		String fileName = filePath.nextLine();
		File inputFile = new File(fileName);
		filePath.close();
		
		String [] labelSet = new String [50];						// stores the labels for individual images

		FileWriter outputFile = null;								// reusable FileWriter to create label lists

		Arrays.fill (labelSet, "null");
		System.out.println(fileName);

		try
		{
			Scanner label = new Scanner (inputFile);				// allows inputing a file of the specified format on the command line	
			int i = 0;
			String delimiter = ",";
			String newFile = new String("");
			String temp = new String("");
			String [] holder;										// array for holding the read results of each line
			while (label.hasNext())
			{
				holder = label.next().split(delimiter);				// put the number and label into the holder array
				temp = holder[0];
				if (! temp.equals(newFile)) {						// when a new image number is found, start a new output file
					if (outputFile != null) outputFile.close();
					newFile = temp;
					outputFile = new FileWriter(newFile + ".txt");	// txt file gets named for image number 
					i = 0;
				}				
				labelSet[i] = holder[1];
				outputFile.write(labelSet[i] + "\n");				// write the label only to the output file
				i++;
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