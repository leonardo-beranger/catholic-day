---
target: site (todas as paginas)
total_score: 22
max_score: 28
na_heuristics: 5,7,10
p0_count: 0
p1_count: 3
timestamp: 2026-08-22T22-35-47Z
slug: site-todas-as-paginas
---
## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | PDF reader shows no loading state on open |
| 2 | Match System / Real World | 4 | Terminology is domain-correct throughout |
| 3 | User Control and Freedom | 3 | No back-to-top/breadcrumb on long trees |
| 4 | Consistency and Standards | 3 | Card component reused for 3 unrelated taxonomies |
| 5 | Error Prevention | n/a | Read-only informational site |
| 6 | Recognition Rather Than Recall | 3 | No breadcrumb in deep trees |
| 7 | Flexibility and Efficiency | n/a | No power-user surface on static site |
| 8 | Aesthetic and Minimalist Design | 3 | Generic card grid reused in 3 places |
| 9 | Error Recovery | 3 | "Fonte" transparency block on Santo do Dia |
| 10 | Help and Documentation | n/a | Not applicable |
| **Total** | | **22/28** | **Good (79%)** |

## Design Specificity Verdict
Split 50/50. Card pattern (eyebrow+title+description) reused identically for site nav (home), hermeneutic Chaves (Profecias), council Eixos (Concilios) - the clearest AI-slop tell. Genuinely authored: Profecias accordion + scripture pills, bilingual Latin/Portuguese quote block (Concilios), Compendio Ser/Estado glossary reasoning pair.

Detector (degraded mode, floor not ceiling): 37 findings/18 pages - overused-font (Inter) x18, em-dash-overuse x17 (advisory, expected in long prose), broken-image x2 (both false positives, JS-hydrated images confirmed loading at runtime).

Orchestrator re-verification: header hamburger-only-at-desktop claim was FALSE (inline nav confirmed at 1280/1568px). Gold label contrast confirmed FIXED (--cor-ouro-texto, ~5.5:1). NEW finding: header .menu overflows its 1120px container at 1060-1750px viewports (confirmed 278px overflow at 1280px, 134px at 1568px via scrollWidth) - real functional break, not caught by either assessment alone.

## Priority Issues
- [P1] Header nav overflows container at 1060-1750px desktop widths (most laptops). Fix: adapt breakpoint or wrap/shrink menu. Command: /impeccable adapt
- [P1] Same card pattern reused for 3 unrelated taxonomies (home nav, Profecias Chaves, Concilios Eixos). Fix: differentiate per usage, reserve card for nav only. Command: /impeccable distill or /impeccable typeset
- [P1] Visible placeholder TODO copy on homepage first paragraph ("Texto de abertura a definir"). Command: /impeccable clarify
- [P2] Inter flagged 18/18 pages by detector as overused/generic font. Command: /impeccable typeset
- [P2] PDF reader has no loading state, blank panel 1-2s. Command: /impeccable harden

## Persona Red Flags
Jordan: first real paragraph on homepage is a visible TODO, undermines rigor positioning.
Sam: no skip-to-content link; nav overflow is itself an accessibility hazard (clipped content vs wrap).
Casey: mobile reflow solid, actually healthier than the 1060-1750px desktop band right now.

## Minor Observations
Compendio "Sinonimos de estudo" under-styled as metadata. Council timeline year format inconsistent, no legend. Santo do Dia "Fonte" transparency block is a good trust pattern worth reusing.

## Questions to Consider
1. Why do 3 top-level pages fall back to the generic card instead of extending the accordion/bilingual-block patterns?
2. Is the desktop nav overflow a recent regression (Santo do Dia layout change) or long-standing?
3. Cost of writing the real homepage opening paragraph now vs shipping the TODO?
