.PHONY: install search gap ask data formula-test paper-a paper-b render-all analysis render journal check-cites

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

paper-a:            ## Makale A'nın tüm sayıları (data hedefinden sonra; ~60 dk)
	python -m engine.data.shot_profile && python -m engine.data.bio && python -m engine.data.advanced && python -m engine.data.assist_network
	cd manuscript/analysis && python thesis_archetypes.py && python roles_final.py && python role_trends.py \
	  && python role_position.py \
	  && python lineup_model.py --roles roles_final_K5.csv --power 100 \
	  && python lineup_model.py --roles roles_final_K4.csv \
	  && python lineup_model.py --roles thesis_archetypes.csv \
	  && python paper_a_summary.py && python figures_paper_a.py
	$(MAKE) formula-test

paper-b:            ## Makale B'nin tüm sayıları (paper-a'dan sonra)
	cd manuscript/analysis && python paper_b_values.py && python ilp_validation.py && python figures_paper_b.py && python figures_paper_b.py --lang tr && python figures_paper_a.py --lang tr

render-all: check-cites ## iki makaleyi docx olarak üret
	cd manuscript && quarto render --to docx
	cd manuscript_b && quarto render --to docx
	cd manuscript_tr && quarto render --to docx
	cd manuscript_b_tr && quarto render --to docx

analysis:
	python manuscript/analysis/run.py

render: analysis check-cites
	cd manuscript && quarto render

journal:            ## make journal J=elsevier | springer | tandf ...
	cd manuscript && quarto add --no-prompt quarto-journals/$(J)

check-cites:        ## metindeki her [@key] references.bib'de olmalı
	python engine/check_cites.py
