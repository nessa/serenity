DOC = presentacion
PDF = $(DOC).pdf

pdf:
	pdflatex $(DOC).tex
	pdflatex $(DOC).tex

clean: 
	$(RM) -f *.ps *.dvi *.aux *.toc \
	*.idx *.ind *.ilg *.log *.out \
	*.snm *.nav *~ *#

clean-all:
	make clean
	$(RM) presentacion.pdf