import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Queue;
import java.util.LinkedList;

class DFA {
    // Retin raspunsurile pentru argumentele `-e` si `-v`
    private boolean acceptsE;
    private boolean isVoid;

    private String initialState;
    private int numNodes = 0;

    // Retin graful care reprezinta AFD-ul atat in forma initiala cat si transpus
    private ArrayList<ArrayList<Integer>> graph;
    private ArrayList<ArrayList<Integer>> graphT;

    // Fac tranzitia de la numele unei stari la indexul acesteia in graf si invers
    private HashMap<String, Integer> stateToIndex;
    private ArrayList<String> indexToState;

    // Multimile de stari necesare in rezolvare
    private HashSet<Integer> accessible;
    private HashSet<Integer> productive;
    private HashSet<Integer> useful;

    private Queue<Integer> productiveQ;

    // Multimi de stari folosite pentru determinarea ciclurilor
    private boolean[] visited;
    private boolean[] open;

    DFA() {
        isVoid          = true;
        initialState    = null;
        acceptsE        = false;

        graph           = new ArrayList<>();
        graphT          = new ArrayList<>();

        stateToIndex    = new HashMap<>();
        indexToState    = new ArrayList<>();

        accessible      = new HashSet<>();
        productive      = new HashSet<>();
        useful          = new HashSet<>();

        productiveQ     = new LinkedList<>();
    }

    /**
     * Adauga o noua stare in AFD.
     *
     * @param state starea nou adaugata
     */
    void addState(String state) {
        indexToState.add(state);
        stateToIndex.put(state, numNodes++);
    }

    /**
     * Creeaza cele doua grafuri folosite.
     */
    void setUpGraphs() {
        for (int i = 0; i != numNodes; ++i) {
            graph.add(new ArrayList<>());
            graphT.add(new ArrayList<>());
        }
    }

    /**
     * Adauga o noua muchie in cele doua grafuri.
     *
     * @param srcStr    nodul sursa sub forma de string
     * @param destStr   nodul destinatie sub forma de string
     */
    void addEdge(final String srcStr, final String destStr) {
        final int src = stateToIndex.get(srcStr);
        final int dest = stateToIndex.get(destStr);

        graph.get(src).add(dest);
        graphT.get(dest).add(src);
    }

    /**
     * Adauga starea initiala a AFD-ului.
     *
     * @param state starea initiala
     */
    void setInitialState(String state) {
        initialState = state;
    }

    /**
     * Determina starile accesibile si le adauga in HashSetul `accessible`.
     */
    void computeAccessible() {
        int init            = stateToIndex.get(initialState);
        Queue<Integer> q    = new LinkedList<>();

        int crtState;
        q.add(init);
        accessible.add(init);

        while (!q.isEmpty()) {
            crtState = q.remove();

            for (int nextState : graph.get(crtState)) {
                if (!accessible.contains(nextState)) {
                    accessible.add(nextState);
                    q.add(nextState);
                }
            }
        }
    }

    /**
     * Verifica daca starea finala este si stare initiala.
     * De asemenea, verifica daca limbajul este vid (starea finala este accesibila).
     *
     * @param state starea finala
     */
    void checkFinalState(String state) {
        int index = stateToIndex.get(state);

        if (initialState.equals(state)) {
            acceptsE = true;
        }

        productiveQ.add(index);
        productive.add(index);

        if (accessible.contains(index)) {
            useful.add(index);
            isVoid = false;
        }
    }

    /**
     * Calculeaza concomitent starile utile si productive.
     * Se foloseste de faptul ca deja sunt cunoscute starile accesibile.
     */
    void computeProductiveUseful() {
        int crtState;

        while (!productiveQ.isEmpty()) {
            crtState = productiveQ.remove();

            for (int nextState : graphT.get(crtState)) {
                if (!productive.contains(nextState)) {
                    productive.add(nextState);

                    if (accessible.contains(nextState)) {
                        useful.add(nextState);
                    }

                    productiveQ.add(nextState);
                }
            }
        }
    }

    /**
     * Determina daca limbajul este finit verficand daca exista un ciclu format din stari utile.
     * Daca o stare dintr-un ciclu este utila, toate starile din acel cilcu vor fi utile.
     *
     * @return `true` daca limbajul este finit, `false` in caz contrar
     */
    boolean isLanguageFinite() {
        visited = new boolean[numNodes];
        open    = new boolean[numNodes];

        return isFinite(stateToIndex.get(initialState));
    }

    /**
     * Aplica DFS pentru a verifica daca o anumita stare face parte dintr-un ciclu ce contine stari
     * utile.
     *
     * @param crtNode   nodul ai caror vecini sunt verificati
     * @return          `false` daca in subarborele nodului curent exista un ciclu format din
     *                  stari utile, `true` in caz contrar
     */
    private boolean isFinite(final int crtNode) {
        open[crtNode] = true;

        for (int nextNode : graph.get(crtNode)) {
            if ((open[nextNode] && useful.contains(crtNode))
                    || (!visited[nextNode] && !open[nextNode] && !isFinite(nextNode))) {
                return false;
            }
        }

        open[crtNode]       = false;
        visited[crtNode]    = true;

        return true;
    }

    // Getteri petnru diversele colectii si variabile folositoare in exteriorul clasei
    boolean acceptsE() {
        return acceptsE;
    }

    HashSet<Integer> getAccessible() {
        return accessible;
    }

    HashSet<Integer> getUseful() {
        return useful;
    }

    String getState(final int index) {
        return indexToState.get(index);
    }

    boolean isLanguageVoid() {
        return isVoid;
    }
}
