.PHONY: install search gap ask analysis render journal check-cites

install:            ## Python bağımlılıkları (+ Quarto ayrıca: https://quarto.org/docs/get-started/)
	pip install -e ".[all]"

search:             ## make search Q="sorgu"
	sspe-search "$(Q)" --year 2010-

gap:                ## make gap Q="araştırma sorusu"
	sspe-gap "$(Q)"

ask:                ## make ask Q="soru"
	sspe-ask "$(Q)"

analysis:
	python manuscript/analysis/run.py

render: analysis check-cites
	cd manuscript && quarto render

journal:            ## make journal J=elsevier | springer | tandf ...
	cd manuscript && quarto add --no-prompt quarto-journals/$(J)

check-cites:        ## metindeki her [@key] references.bib'de olmalı
	python engine/check_cites.py
