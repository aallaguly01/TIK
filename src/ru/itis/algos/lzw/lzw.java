package ru.itis.algos.lzw;

import java.io.*;
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;

public class lzw {

    public HashMap compdic, decompdic;
    String fileName = "D://Ahmedov/original.txt";
    short lastcode = 0, dlastcode = 0;

    lzw() {
        compdic = new HashMap<String, Integer>();
        decompdic = new HashMap<Integer, String>();
        createDictionary();
    }

    public void createDictionary() {
        try {
            short code;
            char ch;
            FileInputStream fis = new FileInputStream(fileName);
            InputStreamReader rdr = new InputStreamReader(fis, "utf-8");
            while ((code = (short) rdr.read()) != -1) {
                ch = (char) code;

                if (!compdic.containsKey(ch)) {
                    compdic.put("" + ch, code);
                    decompdic.put(code, "" + ch);
                    if (code > lastcode) {
                        lastcode = code;
                        dlastcode = code;
                    }
                }
            }
            fis.close();
        } catch (Exception ex) {
            Logger.getLogger(lzw.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    public void compressFile() {
        try {
            short code, codeword;
            char c;
            String s;

            System.out.print("Compressing...");
            FileInputStream fis = new FileInputStream(fileName);
            InputStreamReader rdr = new InputStreamReader(fis, "utf-8");
            FileOutputStream fos = new FileOutputStream(fileName + "1.lzw");
            ObjectOutputStream fout = new ObjectOutputStream(fos);

            s = (char) rdr.read() + "";
            while ((code = (short) rdr.read()) != -1) {
                c = (char) code;

                if (!compdic.containsKey(s + c)) {
                    codeword = Short.parseShort(compdic.get(s).toString());

                    fout.writeShort(codeword);
                    compdic.put(s + c, ++lastcode);
                    s = "" + c;
                } else {
                    s = s + c;
                }
            }

            codeword = Short.parseShort(compdic.get(s).toString());
            fout.writeShort(codeword);
            fout.writeShort(00);

            fout.close();
            fis.close();

            System.out.print("done");

        } catch (Exception ex) {
            Logger.getLogger(lzw.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    public void decompressFile() {
        short priorcode = -1, codeword = -1;
        char c;

        String priorstr, str;
        FileInputStream fis;
        FileWriter fos;
        ObjectInputStream fin;

        try {
            fis = new FileInputStream(fileName + "1.lzw");
            fos = new FileWriter(fileName + "2.txt");
            fin = new ObjectInputStream(fis);

            System.out.print("\nDecompressing...");
            priorcode = fin.readShort();
            fos.write(decompdic.get(priorcode).toString());
            while ((codeword = fin.readShort()) != -1) {
                if(codeword == 00)
                    break;

                priorstr = decompdic.get(priorcode).toString();

                if (decompdic.containsKey(codeword)) {
                    str = decompdic.get(codeword).toString();
                    fos.write(str);
                    decompdic.put(++dlastcode, priorstr + str.charAt(0));
                } else {
                    decompdic.put(++dlastcode, priorstr + priorstr.charAt(0));
                    fos.write(priorstr + priorstr.charAt(0));
                }

                priorcode = codeword;
            }

            fos.close();
            fis.close();
            System.out.print("done\n");

        } catch (Exception ex) {
            //Logger.getLogger(LZW.class.getName()).log(Level.SEVERE, null, ex);
            System.out.println("\n\nError: " + ex.getMessage());
            System.out.print(codeword + " " + priorcode + " " + decompdic.get(133) + " " + dlastcode);
        }
    }

    public static void main(String args[]) {
        lzw lzw = new lzw();
        lzw.compressFile();
        lzw.decompressFile();
    }
}
