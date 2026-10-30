# QA report: BIOINFO/GIW ISCB-Asia 2026 oral talk (submission 241)

Deck `GIW2026_oral241_velocity_reliability_map.pptx` (sha256 2da635bf0be3381d…), 13 main + 4 hidden backup slides, built 2026-10-25 with
academic-conference-presentation skill v1.1.0. Renderer LibreOffice 26.2.5.2, python-pptx 1.0.2.

**Release status: READY for rehearsal, with the open items below.** Venue-machine PowerPoint rendering not tested.

| Gate | Result | Evidence |
|---|---|---|
| 1 Approval and timing | PASS | Approval waived by the user on 2026-10-25 ("완벽하게 ppt 만들어줘" before going out). `plan_check.py` exit 0; main slides 780 s against an 810 s budget (15 min speaking, Q&A separate). Note-length estimate about 12.5–14.5 min at 130–150 words/min. Talk length not yet assigned by the organizers |
| 2 Scientific verification | PASS after fixes | Independent reviewer checked about 200 numbers against the long abstract v2, `results/` and `draft_v2.md`: 0 value mismatches, 18 definition, wording and naming findings. 17 fixed (lag definition labels, same-gene Δρ added to the replication slide, preregistration scope, causal wording in notes, internal IDs, abbreviations). 1 not applied: author name, see below |
| 3 Automated structure | PASS | `check_deck.py`: 0 errors, 141 warnings, all "explicit text below 18 pt" (CI lines, footers, table cells). Each was reviewed in the render |
| 4 Rendered visual review | PASS | All 17 slide PNGs opened at full size after the final build; no overlap, clipping, missing glyph, or shadow. Greek and math glyphs checked in Pretendard |
| 5 Notes and delivery | PASS | English notes embedded on every slide and identical to `GIW2026_oral241_velocity_reliability_map.speaker-notes.md` (verified by `save_deck`) |
| 6 Wording | PASS | No internal IDs or file names in slides or notes after the fixes; abbreviations spelled out at first use (HSPC, BMMC, TT-seq in footer, interquartile range, curvature κ) |

## Findings not applied

- **Author name "Geongyu Lee".** The reviewer pointed to `draft_v2.md` ("Geon gyu Lee"), but `AUTHOR_CONTACTS.md` records
  the author's own correction to "Geongyu Lee" on 2026-09-11 (BIOP02-114 #12213). The newer record wins.

## Open items for the presenter

1. **Cover affiliation.** The presenter is shown as "Pseudo Lab, Seoul", as requested to the organizers on 2026-09-25; the
   program committee's final answer was still pending in the last record. The manuscript uses "Independent Researcher".
2. **Talk length.** Planned for 15 minutes. If the slot is 12 minutes, drop slide 5 (gene dependence) and shorten slide 9 (γ).
3. **Refit stability under the priming definition** is not computed (12 `refit_*.csv` tables are missing); the deck states
   that only the coupled-on duration was refit-tested.
4. **External systems use the coupled-on lag.** The priming interval was recomputed in HSPC only; the replication slide
   says so in its footer.

## Tool limits

python-pptx does not measure text layout; `check_deck.py` checks packaging and outer geometry only. LibreOffice output
is not proof of identical rendering in the venue PowerPoint. Font names do not embed fonts: Pretendard must be installed on
the presenting machine, or use `GIW2026_oral241_velocity_reliability_map.pdf`.
