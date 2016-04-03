import java.io.*;
import java.util.*;

public class StripLine
{
	public static void main (String args[]) throws IOException
	{


		String [] fileList = new String [100];
		Path dir = "/Users/body_LAB/Desktop/ED/NLP\ Files";
		DirectoryStream<Path> stream = Files.newDirectoryStream(dir)
		Scanner input = new Scanner (InputStream stream);
		FileWriter output = new File(input);
		int i = 0;

		FileWriter output = null;
		Arrays.fill (fileList, "null");

		try()
		{
			for (Path file: stream)
			{
				fileList[i] = file.getFileName();
				i++l
			}
		} catch (IOException | DirectoryIteratorException x)
		{
			System.err.println(x);
		}


	}	
}