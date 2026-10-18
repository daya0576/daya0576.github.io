# ADR 0001: Keep the browser default `mark` highlight

- Status: Accepted
- Date: 2026-10-18

## Context

Posts use `==text==`, which Hugo renders as `<mark>`. The theme previously
styled `mark` per color scheme (muted amber in dark, pale yellow in light).
Those styles were removed from `themes/nostyleplease/assets/css/main.scss`,
so `<mark>` now uses the browser default: bright yellow background with
black text, in both light and dark mode.

During a dark-mode style review, restoring a softer dark-mode highlight was
proposed. Henry decided against it.

## Decision

Do not add any `mark` styling. Highlights keep the browser default in both
color schemes.

## Consequences

- Highlights stay high-contrast and stand out sharply against the dark
  page. This is accepted, not a bug.
- Style reviews and palette changes must not reintroduce `mark` colors or
  flag the default highlight as an issue.
- Revisit only if Henry explicitly asks to change the highlight style.
