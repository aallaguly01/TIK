package ru.itis.algos.huffman;

import java.io.*;
import java.util.Hashtable;

public class HuffmanDecoder {

	private Hashtable<String, Character> codeTable = new Hashtable<String, Character>();

	public void createCodeTable(File codes){

		codeTable.clear();
		
		try (BufferedReader br = new BufferedReader(new FileReader(codes))) {
			String line;
			while ((line = br.readLine()) != null) {
				if(line.length() > 2) codeTable.put(line.substring(2), line.charAt(0));
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

	}
	

	// take a bin file and huffman tree and output the decoded words
	public void decodeBinFile(File encoded){
		
		String code = "";

		DataInputStream s;
		FileWriter w;
		try {
			s = new DataInputStream(new FileInputStream(encoded));
			w = new FileWriter("./decoded.txt");
			int data;
			
			while(s.available() > 0){
				data = s.readUnsignedByte();
				for(int i=0; i<8; i++){
					if(codeTable.containsKey(code)){
						w.append(codeTable.get(code));
						code = "";
					}
					if((data & (int)Math.pow(2, 7-i)) == (int)Math.pow(2, 7-i)){
						code += "1";
					}else{
						code += "0";
					}
				}
			}
			s.close();
			w.close();

		} catch (IOException e) {
			e.printStackTrace();
		}

	}

}
