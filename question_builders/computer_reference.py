"""Original practice tasks and Java implementations; not copies of board questions."""
PROGRAMS=[]
def add(name,title,tier,evidence,prompt,logic,traps,code,cases):
 PROGRAMS.append(dict(name=name,title=title,tier=tier,evidence=evidence,prompt=prompt,logic=logic,traps=traps,code=code.strip()+'\n',cases=cases))

add('WaterBill','Class with input, calculation, display and progressive slabs','Highest family priority',
 'First full program in all nine normal papers reviewed; recent Q3 in 2023-2026 [P15-P19, P23-P26].',
 'Define WaterBill with String name, int units and double bill. accept() reads name and non-negative units; calculate() charges Rs 4 per unit for the first 50 units, Rs 6 for the next 50, and Rs 8 thereafter. Add 5% of the calculated charge only when units exceed 100. display() prints name and bill. main() must create an object and invoke the methods. Input: a full name on one line, then units.',
 'Keep fields at class scope. Carry forward the cost of each completed slab, then add the surcharge.',
 'A progressive slab is different from charging every unit at the final rate. Test both sides of each boundary.',
 r'''
import java.util.Scanner;
public class WaterBill {
    String name;
    int units;
    double bill;
    void accept() {
        Scanner sc = new Scanner(System.in);
        name = sc.nextLine();
        units = sc.nextInt();
    }
    void calculate() {
        if (units <= 50) bill = units * 4.0;
        else if (units <= 100)
            bill = 200 + (units - 50) * 6.0;
        else {
            bill = 500 + (units - 100) * 8.0;
            bill += bill * 0.05;
        }
    }
    void display() {
        System.out.println(name);
        System.out.println(bill);
    }
    public static void main(String[] args) {
        WaterBill w = new WaterBill();
        w.accept();
        w.calculate();
        w.display();
    }
}
''',[('Riya Sen\n50\n','Riya Sen\n200.0'),('Riya\n100\n','Riya\n500.0'),('Riya\n101\n','Riya\n533.4')])

add('Revision','Method overloading: pattern, character frequency, formula','Highest family priority',
 'An explicit overloaded-method question appears in all nine normal papers; nested patterns are inside it in every 2023-2026 paper [P23-P26].',
 'Overload show: void show(int rows) prints rows lines, with line i containing i through rows; int show(String text, char target) returns the case-sensitive frequency of target; double show(double radius) returns Math.PI * radius * radius. main() demonstrates show(4), show("BANANA",\'A\') and show(2.0).',
 'The parameter lists select the overload. Use nested for loops for the triangle and a single String traversal for frequency.',
 'Return type alone does not overload a method. show(2) chooses the int overload; show(2.0) chooses double.',
 r'''
public class Revision {
    void show(int rows) {
        for (int i = 1; i <= rows; i++) {
            for (int j = i; j <= rows; j++) {
                if (j > i) System.out.print(" ");
                System.out.print(j);
            }
            System.out.println();
        }
    }
    int show(String text, char target) {
        int count = 0;
        for (int i = 0; i < text.length(); i++)
            if (text.charAt(i) == target) count++;
        return count;
    }
    double show(double radius) {
        return Math.PI * radius * radius;
    }
    public static void main(String[] args) {
        Revision r = new Revision();
        r.show(4);
        System.out.println(r.show("BANANA", 'A'));
        System.out.println(r.show(2.0));
    }
}
''',[('', '1 2 3 4\n2 3 4\n3 4\n4\n3\n12.566370614359172')])

add('CharAudit','Count uppercase, lowercase, digits and other characters','Very high family priority',
 'Character classification was a complete program in 2023 and 2025; Strings also occur in 2024 and 2026 [P23-P26].',
 'Accept a complete line. Count uppercase letters, lowercase letters, digits, and all other characters (including spaces). Print the four counts in that order.',
 'Use an if/else-if chain so each character enters exactly one category.',
 'Do not classify punctuation as lowercase. A space belongs to the explicitly defined other category.',
 r'''
import java.util.Scanner;
public class CharAudit {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();
        int upper = 0, lower = 0, digits = 0, other = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (Character.isUpperCase(c)) upper++;
            else if (Character.isLowerCase(c)) lower++;
            else if (Character.isDigit(c)) digits++;
            else other++;
        }
        System.out.println(upper + " " + lower + " "
                           + digits + " " + other);
    }
}
''',[('AbC_29!\n','2 1 2 2'),('Hi 7\n','1 1 1 1'),('\n','0 0 0 0')])

add('MatrixTotals','Two-dimensional array: row and column sums','Very high family priority',
 'A full 2-D array question occurs in 2024, 2025 and 2026; row/column operations are explicit in the 2027 syllabus [P24-P26, S27].',
 'Read 12 integers into a 3 by 4 array in row order. Print the sum of each row on its own line, followed by the sum of each column on its own line.',
 'Store the matrix first. Reset the row accumulator before each row, and the column accumulator before each column.',
 'Rows have four elements here; columns have three. Do not transpose the loop bounds.',
 r'''
import java.util.Scanner;
public class MatrixTotals {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[][] a = new int[3][4];
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 4; j++)
                a[i][j] = sc.nextInt();
        for (int i = 0; i < 3; i++) {
            int sum = 0;
            for (int j = 0; j < 4; j++) sum += a[i][j];
            System.out.println(sum);
        }
        for (int j = 0; j < 4; j++) {
            int sum = 0;
            for (int i = 0; i < 3; i++) sum += a[i][j];
            System.out.println(sum);
        }
    }
}
''',[('1 2 3 4 5 6 7 8 9 10 11 12\n','10\n26\n42\n15\n18\n21\n24'),('0 0 0 0 0 0 0 0 0 0 0 0\n','0\n0\n0\n0\n0\n0\n0')])

add('BubbleChars','Bubble sort characters and retain the original order','High priority; plausible return candidate',
 'Bubble sort: 2015, 2019 and 2023. It was absent as an explicit long-program algorithm in 2024-2026 [P15, P19, P23-P26].',
 'Accept six single-character tokens. Copy them into a second array. Sort the copy in ascending character-code order using bubble sort only. Display the original and sorted sequences.',
 'After each left-to-right pass, the greatest remaining character reaches the right end.',
 'Use j < length - 1 - pass. Preserve the original by copying elements, not by assigning the same array reference.',
 r'''
import java.util.Scanner;
public class BubbleChars {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        char[] original = new char[6], a = new char[6];
        for (int i = 0; i < 6; i++) {
            original[i] = sc.next().charAt(0);
            a[i] = original[i];
        }
        for (int pass = 0; pass < a.length - 1; pass++)
            for (int j = 0; j < a.length - 1 - pass; j++)
                if (a[j] > a[j + 1]) {
                    char temp = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = temp;
                }
        for (int i = 0; i < 6; i++)
            System.out.print(original[i] + " ");
        System.out.println();
        for (int i = 0; i < 6; i++)
            System.out.print(a[i] + " ");
        System.out.println();
    }
}
''',[('D A C B F E\n','D A C B F E\nA B C D E F'),('a A b B c C\n','a A b B c C\nA B C a b c')])

add('ProductLookup','Linear search with parallel arrays','High priority',
 'Direct lookup in 2016 and explicit linear search in 2023; 2026 uses a related linear frequency scan [P16, P23, P26].',
 'Read positive n, followed by n pairs of one-word product name and price, then a one-word key. Using linear search, print the price of the first matching name, ignoring case. If absent, print Not found.',
 'The index links each name to its price. Stop at the first match.',
 'Use equalsIgnoreCase for String content; == compares references. Unsorted data cannot be searched by binary search safely.',
 r'''
import java.util.Scanner;
public class ProductLookup {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        String[] name = new String[n];
        double[] price = new double[n];
        for (int i = 0; i < n; i++) {
            name[i] = sc.next();
            price[i] = sc.nextDouble();
        }
        String key = sc.next();
        int found = -1;
        for (int i = 0; i < n; i++)
            if (name[i].equalsIgnoreCase(key)) {
                found = i;
                break;
            }
        if (found == -1) System.out.println("Not found");
        else System.out.println(price[found]);
    }
}
''',[('3 pen 12 book 80 bag 450 BOOK\n','80.0'),('2 pen 12 book 80 eraser\n','Not found')])

add('WordFilter','Sentence processing with a start/end predicate','High priority',
 'Word boundaries and predicates recur in 2018-2019, 2022 and 2026; recent String questions vary their condition [P18-P19, P22, P26].',
 'Read a sentence containing only English letters and spaces. Print, in uppercase, each word beginning with a vowel and ending with a consonant. Print Count = followed by the count. Treat A E I O U as vowels. Allow repeated spaces.',
 'Append a trailing space to process the final word. Build each word, test its first and last letters, then reset it.',
 'Check that the word is non-empty before charAt. A consonant is a letter that is not one of the five vowels.',
 r'''
import java.util.Scanner;
public class WordFilter {
    static boolean vowel(char c) {
        return "AEIOU".indexOf(c) >= 0;
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().toUpperCase() + " ";
        String word = "";
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c != ' ') word += c;
            else {
                if (word.length() > 0
                    && vowel(word.charAt(0))
                    && !vowel(word.charAt(word.length() - 1))) {
                    System.out.println(word);
                    count++;
                }
                word = "";
            }
        }
        System.out.println("Count = " + count);
    }
}
''',[('an air echo oar union\n','AN\nAIR\nOAR\nUNION\nCount = 4'),('  ECHO  AREA  \n','Count = 0')])

add('BalancedDigits','An unfamiliar number property defined by the question','High priority',
 'Number-property conditions appear in every 2016-2019 and 2023-2026 normal paper, sometimes inside overloading [P16-P19, P23-P26].',
 'For this original task, call a positive integer balanced if its digit sum is divisible by its number of digits. Read n and print Balanced or Not balanced. Example: 126 has sum 9 and three digits, so it is balanced. Assume n is a positive int.',
 'Use n % 10 for the final digit, n / 10 to remove it, and keep the digit count and sum separately.',
 'Preserve the original if needed for output. Do not learn a number name without its exact supplied definition.',
 r'''
import java.util.Scanner;
public class BalancedDigits {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), temp = n;
        int sum = 0, count = 0;
        while (temp > 0) {
            sum += temp % 10;
            count++;
            temp /= 10;
        }
        if (sum % count == 0)
            System.out.println("Balanced");
        else System.out.println("Not balanced");
    }
}
''',[('126\n','Balanced'),('124\n','Not balanced'),('7\n','Balanced')])

add('SelectionNames','Selection sort names in descending order','High coverage priority',
 'Selection sort occurs in 2017 and 2024. String-array alphabetical sorting remains prescribed [P17, P24, S27].',
 'Read five one-word names, convert them to uppercase, and arrange them in descending alphabetical order using selection sort only. Print one name per line.',
 'For each position find the largest remaining String using compareTo, then swap once.',
 'For descending order, choose a candidate when compareTo is positive. Do not sort using a library routine.',
 r'''
import java.util.Scanner;
public class SelectionNames {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String[] a = new String[5];
        for (int i = 0; i < 5; i++)
            a[i] = sc.next().toUpperCase();
        for (int i = 0; i < a.length - 1; i++) {
            int best = i;
            for (int j = i + 1; j < a.length; j++)
                if (a[j].compareTo(a[best]) > 0) best = j;
            String temp = a[i];
            a[i] = a[best];
            a[best] = temp;
        }
        for (int i = 0; i < a.length; i++)
            System.out.println(a[i]);
    }
}
''',[('Mira Arun Zoya Bina Dev\n','ZOYA\nMIRA\nDEV\nBINA\nARUN'),('A A B B C\n','C\nB\nB\nA\nA')])

add('BinaryCode','Binary search in a sorted character array','High coverage priority',
 'Explicit binary search occurs in 2022 semester 2 and 2025; a recent appearance does not exclude a repeat [P22, P25].',
 'Use the sorted array A D G K N R U Y. Read one character and use binary search to display its one-based position. Print Not found if absent. Comparison is case-sensitive.',
 'Maintain inclusive low/high bounds. Discard the half that cannot contain the key after comparing with the middle element.',
 'Update to mid + 1 or mid - 1, not mid. Character-code order matters; lowercase is not the same as uppercase.',
 r'''
import java.util.Scanner;
public class BinaryCode {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        char[] a = {'A','D','G','K','N','R','U','Y'};
        char key = sc.next().charAt(0);
        int low = 0, high = a.length - 1, found = -1;
        while (low <= high) {
            int mid = (low + high) / 2;
            if (a[mid] == key) {
                found = mid;
                break;
            }
            if (key < a[mid]) high = mid - 1;
            else low = mid + 1;
        }
        if (found < 0) System.out.println("Not found");
        else System.out.println(found + 1);
    }
}
''',[('A\n','1'),('Y\n','8'),('B\n','Not found')])

add('DiagonalCompare','Compare the two diagonal sums of a square matrix','High coverage priority',
 'A diagonal-sum predicate is a complete 2024 question; matrix work continues in 2025-2026 [P24-P26].',
 'Read a 4 by 4 integer matrix. Print the principal diagonal sum, secondary diagonal sum, then Equal or Unequal. Diagonal here means sum comparison only, not a matrix with zero off-diagonal elements.',
 'For row i, principal diagonal is a[i][i]; secondary diagonal is a[i][n - 1 - i].',
 'The question defines the property. Do not impose the mathematical diagonal-matrix definition when asked only to compare sums.',
 r'''
import java.util.Scanner;
public class DiagonalCompare {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[][] a = new int[4][4];
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < 4; j++)
                a[i][j] = sc.nextInt();
        int left = 0, right = 0;
        for (int i = 0; i < 4; i++) {
            left += a[i][i];
            right += a[i][3 - i];
        }
        System.out.println(left + " " + right);
        System.out.println(left == right ? "Equal" : "Unequal");
    }
}
''',[('1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1\n','4 0\nUnequal'),('1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1\n','4 4\nEqual')])

add('SparseCheck','Count zero and non-zero matrix elements','Medium-high priority',
 'Direct matrix predicate in 2026; useful practice for a differently named 2-D condition [P26].',
 'Read a 3 by 4 matrix. Print zero count and non-zero count. Print Sparse only if zeros strictly outnumber non-zeros; otherwise print Not sparse.',
 'Count zeros in a nested loop; obtain non-zeros from 12 minus zeros.',
 'An equal split is not sparse under this definition. Use >, not >=.',
 r'''
import java.util.Scanner;
public class SparseCheck {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[][] a = new int[3][4];
        int zero = 0;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 4; j++) {
                a[i][j] = sc.nextInt();
                if (a[i][j] == 0) zero++;
            }
        int nonzero = 12 - zero;
        System.out.println(zero + " " + nonzero);
        System.out.println(zero > nonzero ? "Sparse" : "Not sparse");
    }
}
''',[('0 0 0 0 0 0 0 1 2 3 4 5\n','7 5\nSparse'),('0 0 0 0 0 0 1 2 3 4 5 6\n','6 6\nNot sparse')])

add('MatrixNorm','Square root of the sum of squares in a matrix','Medium-high priority',
 'A full matrix norm program appeared in 2025; it combines traversal and a supplied formula [P25].',
 'Read a 3 by 3 integer matrix and print sqrt of the sum of squares of all its elements. Use Math.sqrt.',
 'Accumulate squared values in a double, then take exactly one square root at the end.',
 'This is not the sum of individual square roots and not the square of the total sum.',
 r'''
import java.util.Scanner;
public class MatrixNorm {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[][] a = new int[3][3];
        double squares = 0;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) {
                a[i][j] = sc.nextInt();
                squares += (double)a[i][j] * a[i][j];
            }
        System.out.println(Math.sqrt(squares));
    }
}
''',[('3 4 0 0 0 0 0 0 0\n','5.0'),('-3 -4 0 0 0 0 0 0 0\n','5.0')])

add('RotateWord','Transform a word around its first vowel','Medium-high priority',
 '2026 uses a first-consonant rotation; this first-vowel variant practises the underlying String technique [P26].',
 'Read a non-empty alphabetic word and convert to uppercase. Move the letters before its first vowel to the end, then append AY. If there is no vowel, append AY to the original word. Example: TRAIN becomes AINTRAY.',
 'Locate the split point once. Join substring(k), substring(0,k) and the suffix.',
 'Handle vowel at index 0 and no vowel separately. substring end index is excluded.',
 r'''
import java.util.Scanner;
public class RotateWord {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.next().toUpperCase();
        int split = -1;
        for (int i = 0; i < s.length(); i++)
            if ("AEIOU".indexOf(s.charAt(i)) >= 0) {
                split = i;
                break;
            }
        String result = s;
        if (split >= 0)
            result = s.substring(split) + s.substring(0, split);
        System.out.println(result + "AY");
    }
}
''',[('TRAIN\n','AINTRAY'),('APPLE\n','APPLEAY'),('RHYTHM\n','RHYTHMAY')])

add('TitleCase','Change the first letter of each word to uppercase','Medium-high priority',
 'Complete title-case program in 2018; adjacent word-processing work in 2019 and 2026 [P18-P19, P26].',
 'Read a line of letters and spaces. Convert it to lowercase, then capitalize the first letter of every word. Preserve the number of spaces.',
 'Track whether the next non-space character starts a word.',
 'Do not access s.charAt(i - 1) when i is zero. Multiple spaces should not create an empty-word error.',
 r'''
import java.util.Scanner;
public class TitleCase {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().toLowerCase(), result = "";
        boolean start = true;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == ' ') {
                result += c;
                start = true;
            } else {
                result += start ? Character.toUpperCase(c) : c;
                start = false;
            }
        }
        System.out.println(result);
    }
}
''',[('we LEARN java\n','We Learn Java'),('  hello   WORLD\n','  Hello   World')])

add('PalindromeWords','Find palindrome words in a sentence','Medium priority',
 'String palindrome classification appeared in 2016; the traversal transfers to later String predicates [P16, P23-P26].',
 'Read letters and spaces. Print each palindrome word of at least two letters, ignoring case; display in uppercase. Repeated spaces are allowed. Print the final count.',
 'Extract words, reverse each word using charAt, and compare using equals.',
 'One-letter words do not qualify in this task. Reset the word after each delimiter.',
 r'''
import java.util.Scanner;
public class PalindromeWords {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().toUpperCase() + " ";
        String word = "";
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c != ' ') word += c;
            else {
                String reverse = "";
                for (int j = word.length() - 1; j >= 0; j--)
                    reverse += word.charAt(j);
                if (word.length() >= 2 && word.equals(reverse)) {
                    System.out.println(word);
                    count++;
                }
                word = "";
            }
        }
        System.out.println("Count = " + count);
    }
}
''',[('LEVEL IS A CIVIC DUTY\n','LEVEL\nCIVIC\nCount = 2'),('A I NO\n','Count = 0')])

add('ArraySummary','One-dimensional array: minimum, maximum and total','Medium priority',
 'Array aggregation in 2017, parallel-array averages in 2018, grouped totals in 2023 and frequency in 2026 [P17-P18, P23, P26].',
 'Read positive n, then n integers into an array. Print minimum, maximum and total in that order. Values can be negative.',
 'Initialize min and max from the first array element; add every element once.',
 'Initializing max to zero fails when every input is negative. Use long for the total.',
 r'''
import java.util.Scanner;
public class ArraySummary {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = sc.nextInt();
        int min = a[0], max = a[0];
        long total = 0;
        for (int i = 0; i < n; i++) {
            if (a[i] < min) min = a[i];
            if (a[i] > max) max = a[i];
            total += a[i];
        }
        System.out.println(min + " " + max + " " + total);
    }
}
''',[('4 -8 -2 -5 -1\n','-8 -1 -16'),('1 7\n','7 7 7')])

add('BookDiscount','Constructor overloading with a bracket-based discount','Medium priority',
 'Explicit constructors occur in the 2016/2019 class programs and in 2024/2025 Section A; practise constructors even when Q3 omits them [P16, P19, P24-P25].',
 'Define fields String name, double price, double payable. Supply a no-argument constructor and BookDiscount(String name, double price). calculate() gives a whole-price discount of 5% up to Rs 1000, 10% above 1000 up to 3000, and 15% above 3000. display() prints name and payable. main() reads name then price and uses the parameterized constructor.',
 'Select one discount percentage for the entire price; this is not a progressive slab.',
 'Constructor names exactly match the class and have no return type. this.name distinguishes the field from the parameter.',
 r'''
import java.util.Scanner;
public class BookDiscount {
    String name;
    double price, payable;
    BookDiscount() { this("", 0); }
    BookDiscount(String name, double price) {
        this.name = name;
        this.price = price;
    }
    void calculate() {
        double rate;
        if (price <= 1000) rate = 5;
        else if (price <= 3000) rate = 10;
        else rate = 15;
        payable = price - price * rate / 100.0;
    }
    void display() {
        System.out.println(name);
        System.out.println(payable);
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String name = sc.nextLine();
        double price = sc.nextDouble();
        BookDiscount b = new BookDiscount(name, price);
        b.calculate();
        b.display();
    }
}
''',[('Java Basics\n1000\n','Java Basics\n950.0'),('Java\n3000\n','Java\n2700.0'),('Java\n4000\n','Java\n3400.0')])

add('MenuSeries','Menu-driven alternating powers or factorial series','Medium priority',
 'Standalone menus in 2015-2019; series also appear inside overloaded methods in 2016, 2019 and 2025 [P15-P19, P25].',
 'Read choice. Choice 1 reads n and x, then prints x - x^2 + x^3 - ... through n terms. Choice 2 reads n and prints 1! + 2! + ... + n!. Assume 1 <= n <= 12. For any other choice print Invalid choice. Use switch.',
 'Use the term position for alternating sign. For factorials, carry a running product and add it after each multiplication.',
 'Use a floating-point accumulator for powers. Initialize factorial to 1 outside the loop. Include break and default.',
 r'''
import java.util.Scanner;
public class MenuSeries {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int choice = sc.nextInt();
        switch (choice) {
            case 1: {
                int n = sc.nextInt();
                double x = sc.nextDouble(), sum = 0;
                for (int i = 1; i <= n; i++) {
                    double term = Math.pow(x, i);
                    if (i % 2 == 1) sum += term;
                    else sum -= term;
                }
                System.out.println(sum);
                break;
            }
            case 2: {
                int n = sc.nextInt();
                long factorial = 1, sum = 0;
                for (int i = 1; i <= n; i++) {
                    factorial *= i;
                    sum += factorial;
                }
                System.out.println(sum);
                break;
            }
            default: System.out.println("Invalid choice");
        }
    }
}
''',[('1 3 2\n','6.0'),('2 4\n','33'),('9\n','Invalid choice')])

add('PronicCheck','Test a product-of-consecutive-integers condition','Medium priority; broadens number practice',
 'A Pronic test appeared in 2018. Later papers use different named number conditions; the skill is translating a definition [P18, P24-P26].',
 'Read an integer n with 0 <= n <= 1000000000. Print Pronic if n = k * (k + 1) for a non-negative integer k; otherwise print Not pronic. Under this definition, zero qualifies.',
 'Try non-negative k until its product exceeds n. Use long for multiplication.',
 'Do not require memorizing the number name. Include the equality endpoint and define the zero case.',
 r'''
import java.util.Scanner;
public class PronicCheck {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        long n = sc.nextLong();
        boolean found = false;
        for (long k = 0; k * (k + 1) <= n; k++)
            if (k * (k + 1) == n) {
                found = true;
                break;
            }
        System.out.println(found ? "Pronic" : "Not pronic");
    }
}
''',[('42\n','Pronic'),('43\n','Not pronic'),('0\n','Pronic')])

assert len(PROGRAMS)==20
