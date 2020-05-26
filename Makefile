all: cdc-gen-latex.py 
	./cdc-gen-latex.py input.xslx > output.tex
	xelatex output.tex -o output.pdf
