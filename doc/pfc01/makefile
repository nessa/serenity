# -*- coding: utf-8  -*-
#---------------------------------------------------------
# Noelia Sales Montes (c) 2010
#---------------------------------------------------------
# This program is free software: you can redistribute
# it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software
# Foundation, either version 3 of the License, or any
# later version.

# This program is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# You should have received a copy of the GNU General
# Public License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

# Contacto:
#            noelia.salesmontes@gmail.com
#---------------------------------------------------------
NOM = pfc01
DOC = $(NOM).tex

PDF = pdflatex --shell-escape
LATEX = latex --shell-escape
DVI = dvipdf
SHOW = evince


# Compilación por defecto = Códigos + Pdflatex + Bibtex

pdf:
	$(PDF) $(DOC) && $(PDF) $(DOC)

latex:
	$(LATEX) $(DOC) && $(LATEX) $(DOC)

# Pasa de .dvi a .pdf
dvi-pdf:
	$(DVI) $(NOM).tex



#---------------------------------------------------------
# LIMPIEZA
clean:
	$(RM) *.aux *.toc *.log \
	*.lof *.lot *.out *.bbl \
	*.maf *.mtc* *.blg *.pyg \
	*~ *\#
	$(RM) -r auto

clean-all:
	make clean
	$(RM) $(NOM).dvi

#---------------------------------------------------------
