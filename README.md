# LFA
Tema la LFA - 2020

Fiecare cerinta este rezolvata din prima parsare a inputului. In anumite stari
ale *AFD*-ului care parseaza fisierul de input, se stocheaza/calculeaza
structurile necesare rezolvarii respectivelor cerinte.

## -e
Pur si simplu se verifica daca vreuna dintre starile finale este cea initiala.

## -a si -u
Aceste cerinte se rezolva similar: parcurgand cu un *BFS* din starea initiala,
respectiv din starile finale graful ce reprezinta *AFD*-ul, respectiv acelasi graf
transpus. Din prima parcurgere rezulta starile accesibile, iar din cea de-a doua
cele productive. Starile utile sunt intersectia acestor doua multimi.

## -v
Limbajul este vid daca starile finale nu sunt accesibile. La citirea fiecarei
stari finale se verifica daca aceasta este si accesibila.

## -f
Se testeaza cu un *DFS* care verifica daca exista cicluri in AFD. Din moment ce
daca un nod dintr-un ciclu este util, toate nodurile sunt utile, in momentul in
care se depisteaza un ciclu se verifica un singur nod.