ICSE 2027 study pack — worked-answer edition
Open index.html directly, or run node serve_icse_site.js.
Each subject has subjects/<subject>/research and subjects/<subject>/practice.
Twenty fixed papers per subject; answers unlock after marking a paper complete. Revised-paper completion is tracked separately from the earlier edition.
Question banks now show worked calculations, Java traces/tables, model writing and part-by-part literature answers. Short one-mark answers remain concise.
The writing repertoire includes ten English compositions and letters, and ten Hindi compositions and letters, with complete original models. Weak Hindi writing templates were removed instead of padding their answers.
Geography: open Maps & topo sheets for 70 location exercises and original Survey of India PDFs G43S7 and G43S10. Grid limits/editions matter; match an exercise to its supplied sheet. Keep assets/maps with the pack for offline access to the complete sheets.
Downloaded HTML papers embed their images; Print / Save PDF waits for question images to load. Physics includes schematic circuits, levers and completed ray constructions.
Use Needs work / Got it / Correct on retest to build a mistake notebook and spaced review queue. Progress & mistakes shows family coverage and saved paper scores. The writing timer survives navigation/reload; self-mark after completion, then save your score and revision note. Backups can be exported/restored as JSON.
Focused practice offers 5, 10 or 20 questions, prioritising mistakes and due reviews with different families before extra variants. Working and correction notes save automatically and appear in Progress & mistakes; backups include them. Correct on retest requires at least 24 hours since the previous rating.
Question bank: filter by family or select One example per family to check breadth.
English grammar: 500 answers across 50 joining/transformation patterns now explain the construction and its common error. Downloaded solutions include checking advice.
Revised papers use new completion/timer/score records because question selections changed. Bank reviews and checked questions are preserved; older paper records remain in storage and backups.
A 95% target is tracked through timed practice, coverage and error correction; it is not a guaranteed examination result. Scores and mastery labels are self-recorded.
All practice text is original. Numerical variants are grouped by family, not presented as thousands of distinct concepts.
Evidence: 2023–2026 all-subject inventory and 2027 syllabus/specimen, plus Geography sheet audit for 2017–2026 with 2016 context. Cancelled and split-semester years are labelled separately. Evergreen publisher listing was checked; the full book was not publicly available to audit.
Build: python -X utf8 build_exam_pack.py
Visuals: python -X utf8 build_visuals.py
Checks: python -X utf8 test_exam_pack.py; node test_browser.cjs; node test_study_features.cjs
