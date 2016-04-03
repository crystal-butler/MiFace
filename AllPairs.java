import java.io.*;
import java.util.*;

public class AllPairs
{
	public static void main(String args[]) throws IOException
	{
		Scanner filePath = new Scanner (System.in);
		System.out.println("Input filename: ");
		System.out.flush();
		String fileName = filePath.nextLine();
		File inputFile = new File(fileName);
		
		String [] labelSet = new String [40];

		FileWriter outputFile = null;

		Arrays.fill (labelSet, "null");
		System.out.println(fileName);

		try
		{
			Scanner label = new Scanner (inputFile);
			outputFile = new FileWriter(inputFile + ".out.txt");

			int a = 0;
			while (label.hasNext())
			{
				labelSet[a]=label.next();
				a++;
			}

			// System.out.println("label set length = " + labelSet.length);

			int i = 0;
			for (i=0; i<labelSet.length; i++)
			{
				if (!labelSet[i].equals("null"))
				{
					for (int j=(i+1); j<labelSet.length; j++)
					{
						// System.out.println("i = " + i);
						// System.out.println("j = " + j);
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