DOC = presentacion
PDF = $(DOC).pdf

pdf:
	pdflatex --shell-escape $(DOC).tex
	pdflatex --shell-escape $(DOC).tex

clean: 
	$(RM) -f *.ps *.dvi *.aux *.toc \
	*.idx *.ind *.ilg *.log *.out \
	*.snm *.nav *~ *#

clean-all:
	make clean
	$(RM) presentacion.pdf
