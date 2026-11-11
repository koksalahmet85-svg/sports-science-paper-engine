.PHONY: install search gap ask data formula-test paper-a analysis render journal check-cites

install:            ## Python bağımlılıkları (+ Quarto ayrıca: https://quarto.org/docs/get-started/)
	pip install -e ".[all]"

search:             ## make search Q="sorgu"
	sspe-search "$(Q)" --year 2010-

gap:                ## make gap Q="araştırma sorusu"
	sspe-gap "$(Q)"

ask:                ## make ask Q="soru"
	sspe-ask "$(Q)"

data:               ## EuroLeague API → data/raw (≈40 MB, ~25 dk) → data/processed
	python -m engine.data.euroleague && python -m engine.data.build_tables

formula-test:       ## OPEN_QUESTIONS #2: 4 varyant × 1000 permütasyon
	for m in corrected thesis; do for d in 0 2; do python manuscript/analysis/archetype_formulas.py --stints $$m --min-dur $$d --B 1000 > /dev/null; done; done
	python manuscript/analysis/report_formula_test.py

paper-a:            ## Makale A'nın tüm sayıları (data hedefinden sonra; ~30 dk)
	python -m engine.data.shot_profile && python -m engine.data.bio && python -m engine.data.advanced && python -m engine.data.assist_network
	cd manuscript/analysis && python thesis_archetypes.py && python archetypes_v2.py --features full --kmin 4 --kmax 8 --K 5 --method gmm \
	  && python archetypes_v2.py --features advanced --kmin 4 --kmax 4 --K 4 --method gmm \
	  && python role_position.py && python lineup_model.py --roles archetypes_v2_full.csv \
	  && python lineup_model.py --roles archetypes_v2_advanced.csv && python paper_a_summary.py
	$(MAKE) formula-test

analysis:
	python manuscript/analysis/run.py

render: analysis check-cites
	cd manuscript && quarto render

journal:            ## make journal J=elsevier | springer | tandf ...
	cd manuscript && quarto add --no-prompt quarto-journals/$(J)

check-cites:        ## metindeki her [@key] references.bib'de olmalı
	python engine/check_cites.py
