import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Main {
    public static void main(String [] args) {
        if (args.length != 1) {
            System.err.println("Argument error");
        }

        // Se creeaza AFD-ul ce va fi folosit pentru rezolvarea cerintelor
        DFA dfa = new DFA();

        Flexer scanner;

        try {
            BufferedReader br   = new BufferedReader(new FileReader("dfa"));
            scanner             = new Flexer(br);

            scanner.setDFA(dfa);
            scanner.yylex();
            br.close();
        } catch (IOException e) {
            scanner = null;
            e.printStackTrace();
        }

        if (scanner == null) {
            return;
        }

        // Se raspunde la intrebarea corespunzatoare argumentului primit
        switch(args[0]) {
            case "-e":
                if (dfa.acceptsE()) {
                    System.out.println("Yes");
                } else {
                    System.out.println("No");
                }
                break;

            case "-a":
                for (int state : dfa.getAccessible()) {
                    System.out.println(dfa.getState(state));
                }
                break;

            case "-u":
                for (int state : dfa.getUseful()) {
                    System.out.println(dfa.getState(state));
                }
                break;

            case "-v":
                if (dfa.isLanguageVoid()) {
                    System.out.println("Yes");
                } else {
                    System.out.println("No");
                }
                break;

            case "-f":
                if (dfa.isLanguageFinite()) {
                    System.out.println("Yes");
                } else {
                    System.out.println("No");
                }
                break;

            default:
                System.err.println("Argument error");
                System.exit(1);
                break;
        }
    }
}
