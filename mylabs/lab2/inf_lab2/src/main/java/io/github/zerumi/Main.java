package io.github.zerumi;

import java.util.Arrays;
import java.util.Scanner;
import java.util.stream.IntStream;

public class Main {
    public static void main(String[] args) {
        try {
            System.out.print("Enter code: ");

            Scanner scanner = new Scanner(System.in);
            int[] code = Arrays.stream(scanner.nextLine().split("")).mapToInt(Integer::parseInt).toArray();

            int[][] matrix = buildMatrix(code);
            int[] syndrome = getSyndrome(matrix);

            int[] rightCode = correctCode(code, syndrome);
            System.out.println("Correct message: " + Arrays.toString(getInformalBits(rightCode)));

        } catch (RuntimeException e) {
            e.printStackTrace();
        }
    }

    public static int[] getInformalBits(int[] fullCode)
    {
        return IntStream.range(1, fullCode.length + 1).filter(x -> Math.log(x) / Math.log(2) % 1 != 0).map(x -> fullCode[x - 1]).toArray();
    }

    public static int[][] buildMatrix(int[] fullCode)
    {
        double logOperation = Math.log(fullCode.length) / Math.log(2);
        int[][] result = new int[(int) Math.ceil(logOperation % 1 == 0 ? ++logOperation : logOperation) + 1][fullCode.length];

        System.arraycopy(fullCode, 0, result[0], 0, fullCode.length);
        for (int i = 1; i < result.length; i++)
        {
            int currentN = (int) Math.pow(2, i - 1);
            for (int j = currentN - 1; j < result[i].length; j += 2 * currentN) {
                for (int k = j; k < Math.min(result[i].length, (j + currentN)); k++) {
                    result[i][k] = 1;
                }
            }
        }

        return result;
    }

    public static int[] getSyndrome(int[][] matrix) {
        int[] result = new int[matrix.length - 1];

        for (int i = 1; i < matrix.length; i++) {
            int nowI = i;
            result[i - 1] = IntStream.range(0, matrix[i].length).filter(j -> matrix[nowI][j] == 1).map(x -> matrix[0][x]).sum() % 2;
        }

        return result;
    }

    public static int[] correctCode(int[] code, int[] syndrome)
    {
        int errCode = 0;
        for (int i = 0; i < syndrome.length; i++) {
            errCode += syndrome[i] * Math.pow(2, i);
        }

        if (errCode == 0) return code;

        System.out.println("Found incorrect bit: " + errCode + " (" + getNameOfBit(errCode--) + ")");
        code[errCode] = (code[errCode] + 1) % 2;

        return code;
    }

    public static String getNameOfBit(int position)
    {
        double logOperation = Math.log(position) / Math.log(2);
        return logOperation % 1 == 0 ? "r" + (int)logOperation + 1 : "i" + (int)(position - Math.ceil(logOperation));
    }
}