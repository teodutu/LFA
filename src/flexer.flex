import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Queue;
import java.util.LinkedList;

%%

%class Flexer
%unicode
/*%debug*/
%int
/*%line*/
/*%column*/

%{
    public boolean acceptsE = false;
    public String initialState = null;

    public int numNodes = 0;
    private int src;
    private int dst;

    public ArrayList<ArrayList<Integer>> graph;
    public ArrayList<ArrayList<Integer>> graphT;

    public HashMap<String, Integer> stateToIndex;
    public ArrayList<String> indexToState;

    public HashSet<Integer> accessible;
    public HashSet<Integer> productive;
    public HashSet<Integer> useful;
    public HashSet<Integer> finalStates;

    private Queue<Integer> productiveQ;
%}


LineTerminator = \r|\n|\r\n
WS = {LineTerminator} | [ \t\f]
special = "`"|"-"|"="|"["|"]"|";"|"'"|"\\"|"."|"/"|"~"|"!"|"@"|"#"|"$"|"%"|"^"|"&"|"*"|"_"|"+"|":"|"\""|"|"|"<"|">"|"?"
Symbol = [:uppercase:] | [:lowercase:] | [:digit:] | {special}
Name = ([:uppercase:] | [:lowercase:] | [:digit:] | "_")+

%state STARTK ELEMK STOPK SEPKS STARTS INITS ELEMS STOPS SEPSD STARTD INITD ELEMD SRCT SEPSST SYMT SEPSDT DESTT ENDT ENDD STOPD SEPDS SS SEPSF STARTF INITF ELEMF STOPF ENDDFA FINAL

%state DFA STATES STSEP ALPHABET ALSEP DELTA DSEP START STASE STOP STOSE

%%
{WS}	{}
<YYINITIAL>"(" {
    stateToIndex = new HashMap<>();
    indexToState = new ArrayList<>();

    yybegin(STARTK);
}

<STARTK> "{" {
    yybegin(ELEMK);
}

<ELEMK> {Name} {
    indexToState.add(yytext());
    stateToIndex.put(yytext(), numNodes++);

	yybegin(STOPK);
}

<STOPK> {
    "}" {
        yybegin(SEPKS);
    }
    ","	{
        yybegin(ELEMK);
    }
}

<SEPKS> "," {
    yybegin(STARTS);
}

<STARTS> "{" {
    graph   = new ArrayList<>();
    graphT  = new ArrayList<>();

    for (int i = 0; i != numNodes; ++i) {
        graph.add(new ArrayList<>());
        graphT.add(new ArrayList<>());
    }

    yybegin(INITS);
}

<INITS> "}" {
    yybegin(SEPSD);
}

<ELEMS, INITS> {Symbol}	{
    yybegin(STOPS);
}

<STOPS> {
    ","	{
        yybegin(ELEMS);
    }
    "}" {
        yybegin(SEPSD);
    }
}

<SEPSD> "," {
    yybegin(STARTD);
}

<STARTD> "(" {
    yybegin(INITD);
}

<INITD> ")" {
    yybegin(SEPDS);
}

<ELEMD,INITD> "(" {
    yybegin(SRCT);
}

<SRCT> {Name} {
    src = stateToIndex.get(yytext());

    yybegin(SEPSST);
}


<SEPSST> "," {
    yybegin(SYMT);
}

<SYMT> {Symbol} {
    yybegin(SEPSDT);
}

<SEPSDT> "," {
    yybegin(DESTT);
}

<DESTT> {Name} {
    dst = stateToIndex.get(yytext());

    graph.get(src).add(dst);
    graphT.get(dst).add(src);

    yybegin(ENDT);
}

<ENDT> ")" {
    yybegin(STOPD);
}

<STOPD> {
    "," {
        yybegin(ELEMD);
    }
    ")" {
        yybegin(SEPDS);
    }
}

<SEPDS> "," {
    yybegin(SS);
}

<SS> {Name} {
    initialState        = yytext();
    int init            = stateToIndex.get(initialState);
    Queue<Integer> q    = new LinkedList<>();
    accessible          = new HashSet<>();

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

    yybegin(SEPSF);
}

<SEPSF> "," {
    productiveQ = new LinkedList<>();
    productive  = new HashSet<>();
    finalStates = new HashSet<>();
    useful      = new HashSet<>();


    yybegin(STARTF);
}

<STARTF> "{" {
    yybegin(INITF);
}

<INITF> "}" {
    yybegin(ENDDFA);
}

<INITF,ELEMF> {Name} {
    String crtFinal = yytext();
    int crtFinalIndex = stateToIndex.get(crtFinal);

    if (initialState.equals(crtFinal)) {
        acceptsE = true;
    }

    productiveQ.add(crtFinalIndex);
    productive.add(crtFinalIndex);
    finalStates.add(crtFinalIndex);

    if (accessible.contains(crtFinalIndex)) {
        useful.add(crtFinalIndex);
    }

    yybegin(STOPF);
}

<STOPF> {
    "," {
        yybegin(ELEMF);
    }
    "}" {
        yybegin(ENDDFA);
    }
}
<ENDDFA> ")" {
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

    return 0;
}

. {
    System.err.println("Syntax error");
    System.exit(0);
}
