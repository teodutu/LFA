import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;

public class Main {
    private static boolean[] visited;
    private static boolean[] open;

    private static boolean isFinite(
            final ArrayList<ArrayList<Integer>> graph,
            final HashSet<Integer> useful,
            final int crtNode) {
        open[crtNode] = true;

        for (int nextNode : graph.get(crtNode)) {
            if ((open[nextNode] && useful.contains(crtNode))
                || (!visited[nextNode] && !open[nextNode] && isFinite(graph, useful, nextNode))) {
                return true;
            }
        }

        open[crtNode]       = false;
        visited[crtNode]    = true;

        return false;
    }

    public static void main(String [] args) {
        if (args.length != 1) {
            System.err.println("Argument error");
        }

        Flexer scanner;

        try {
            BufferedReader br   = new BufferedReader(new FileReader("dfa"));
            scanner             = new Flexer(br);

            scanner.yylex();
            br.close();


        } catch (IOException e) {
            scanner = null;
            e.printStackTrace();
        }

        if (scanner == null) {
            return;
        }

        switch(args[0]) {
            case "-e":
                if (scanner.acceptsE) {
                    System.out.println("Yes");
                } else {
                    System.out.println("No");
                }
                break;
            case "-a":
                for (int state : scanner.accessible) {
                    System.out.println(scanner.indexToState.get(state));
                }
                break;
            case "-u":
                for (int state : scanner.useful) {
                    System.out.println(scanner.indexToState.get(state));
                }
                break;
            case "-v":
                boolean voidLanguage = true;

                for (int state : scanner.finalStates) {
                    if (scanner.accessible.contains(state)) {
                        voidLanguage = false;
                        break;
                    }
                }

                if (voidLanguage) {
                    System.out.println("Yes");
                } else {
                    System.out.println("No");
                }

                break;
            case "-f":
                visited = new boolean[scanner.numNodes];
                open    = new boolean[scanner.numNodes];

                if (isFinite(
                        scanner.graph,
                        scanner.useful,
                        scanner.stateToIndex.get(scanner.initialState))) {
                    System.out.println("No");
                } else {
                    System.out.println("Yes");
                }

                break;
            default:
                System.err.println("Argument error");
                System.exit(1);
        }
    }
}
