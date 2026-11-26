# Build the documentation site. The work is in build_docs.py.
#
#   make html     build both languages into build/html
#   make strict   the same, but stop when Sphinx gives a warning
#   make serve    serve build/html at http://localhost:8000
#   make clean    remove the build output and the generated API pages

PYTHON ?= python

.PHONY: html strict serve clean

html:
	$(PYTHON) build_docs.py

strict:
	$(PYTHON) build_docs.py --strict

serve:
	$(PYTHON) -m http.server 8000 -d build/html

clean:
	rm -rf build en/apidocs zh/apidocs
