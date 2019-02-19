// author: Crystal Butler
//06/02/2015

import java.io.*;
import java.util.*;
import java.util.Scanner;

public class ImageFiles
{
	public static void main(String args[]) throws IOException
	{
		// read in a Directory name: must contain only files with int scores
		Scanner filePath = new Scanner (System.in);
		System.out.println("Input filename: ");
		System.out.flush();
		String fileName = filePath.nextLine();
		File inputFile = new File(fileName);
		String imageNum;
		String temp;
		String label;

		try
		{
			Scanner imageLabels = new Scanner(inputFile);
			imageNum = imageLabels.next();
			while (imageLabels.hasNextLine())
			{
				temp = imageNum;
				System.out.println("temp is " + temp);
				System.out.println("imageNum is " + imageNum);

				Writer outputFile = new FileWriter(imageNum + ".txt");

				while (imageNum.equals(temp))
				{
					label = imageLabels.next();
					System.out.println("imageLabels is " + label);
					outputFile.write(label + "\n");
					if(imageLabels.hasNextLine())
					{
						imageNum = imageLabels.next();
					} else {
						break;
					}
					
					System.out.println("imageNum2 is " + imageNum);
				}

				outputFile.close();
			}

			imageLabels.close();

		}
		catch (FileNotFoundException e) 
		{
			e.printStackTrace();
		}

	}
}
