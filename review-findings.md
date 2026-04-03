## REVIEW CLEAN
## Code Review Audit: AutoGRADE (autograde.html)
### Date: 2026-04-03
### Summary: 0 P0, 0 P1, 3 P2

---

#### P0 -- Critical

None.

#### P1 -- Important

None.

#### P2 -- Minor / Enhancement

- **P2-1** [Accessibility]: Skip-nav link exists but uses inline style toggle approach (good). Focus management on modal is properly implemented with keyboard trap (Esc, Tab cycling). No issues found.

- **P2-2** [Statistics]: GRADE downgrade thresholds are heuristic-based (RoB: >30% serious, >50% very serious; I2: >40% serious, >75% very serious). These are clearly documented in the About modal and match published GRADE guidance. The imprecision domain correctly checks CI crossing null and OIS status. Publication bias correctly uses Egger's p-value thresholds with small-study warnings.

- **P2-3** [Enhancement]: No CSV export exists (JSON only). The JSON export properly creates and revokes Blob URLs. If CSV export is added in the future, ensure CSV injection guards are applied (prepend `'` to cells starting with `=+@\t\r`, NOT `-`).

#### Checklist

- [x] `</html>` closing tag present (line 551)
- [x] Div balance: 45/45 (excluding JS)
- [x] No literal `</script>` inside script blocks
- [x] `escapeHtml` escapes `& < > " '` (line 240-241) -- covers attribute contexts
- [x] Blob URLs revoked after use (line 480)
- [x] Skip-nav link present (line 81)
- [x] Modal keyboard trap with cleanup (lines 530-545)
- [x] `aria-live="polite"` on results card (line 165)
- [x] Dark mode properly toggles via `data-theme` attribute
- [x] GRADE formula: RCT starts at 4, OBS at 2, clamp [1,4] -- correct
- [x] OR absolute effect: `eer = cer * est / (1 - cer + cer * est)` -- correct Peto formula
- [x] NNT = 1/ARR -- correct
