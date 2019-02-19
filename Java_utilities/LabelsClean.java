/* 12/05/2016 Crystal Butler
 * This class takes as input a text file with a single string per line,
 * comprising words rejected by the GloVe cosine similarity algorithm based
 * on the glove.6B.vocab.txt vocabulary. It additionally takes the name
 * of a directory containing MiFace expression labeling study label lists
 * for removal of the words from the rejecct list. It outputs a cleaned version
 * of the label lists.
 */

import java.io.*;
import java.util.*;

public class LabelsClean {

	public static void main(String[] args) throws IOException {

		// read reject word file and label list directory from standard in
		Scanner readPath = new Scanner(System.in);
		System.out.println("Enter rejected words filename:");
		System.out.flush();
		String fileName = readPath.nextLine();
		File rejectFile = new File(fileName);
		
		Scanner dirPath = new Scanner(System.in);
		System.out.println("Input directory of label files to clean of rejects:");
		System.out.flush();
		String dirName = dirPath.nextLine();

		// declare an output file for cleaned results
		FileWriter outputFile = null;

		// has a reject word been found in label file?
		boolean match;
		
		// read all label file names into an array
		File[] labelFiles = new File(dirName).listFiles();

		// read all reject words into a Vector<>
		Vector<String> rejects = new Vector<>();
		try {
			Scanner readRejects = new Scanner(rejectFile);
			while(readRejects.hasNext()) {
				rejects.add(readRejects.nextLine());
			}
			readRejects.close();
		}
		catch (FileNotFoundException e) {
			e.printStackTrace();
		}

		// clean all the files in the label list directory
		for (File file : labelFiles) {

			try {
				String labelFile = file.getName();
				File inputFile = new File(dirName + "/" + labelFile);
				Scanner label = new Scanner(inputFile);
				String checkLabel;
				outputFile = new FileWriter(inputFile + "_clean.txt");

				// check the labels in a file against reject words;
				// write good labels out to a new file
				while (label.hasNext()) {
					match = false;
					checkLabel = label.nextLine();
					for (String reject : rejects) {
						if (! reject.equals(checkLabel)) continue;
						else {
							match = true;
							break;
						}
					}
					if (! match) {
						outputFile.write(checkLabel + "\n");
					}
				}
				label.close();
			}
			catch (FileNotFoundException e) {
				e.printStackTrace();
			}
			finally {
				if (outputFile != null) {
					outputFile.close();
				}
			}
		}

		readPath.close();
	}
}