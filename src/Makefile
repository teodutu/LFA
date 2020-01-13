JFLAGS = -g
JC = javac
JVM = java
JFLEX = ./lib/jflex-1.6.1.jar

all: build

Flexer.java: flexer.flex
	jflex --nobak $< 1>&2

sources = $(wildcard *.java)
classes = $(sources:.java=.class)

build: Flexer.java $(classes)

run: build
	$(JVM) Main $(arg)

.PHONY: clean
clean :
	rm -f *.class Flexer.java *~
%.class : %.java
	$(JC) $(JFLAGS) $<
