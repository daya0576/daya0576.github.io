# ADR 0003: Keep the boxed blocks and the table grid

- Status: Accepted
- Date: 2026-10-18

## Context

A dark-mode style review proposed removing the remaining boxes:

- `.read-more`: the series "Read more" section, a `1px solid`
  `currentColor` box.
- `details` (and `.toc`): the same `1px solid` box with `1rem` padding.
- Tables: full cell grid with a `$surface` header background. A Tailwind
  Typography style table (horizontal rules only) was proposed.

Henry likes the original thin boxes as they are: minimal.

## Decision

Keep all three unchanged in `themes/nostyleplease/assets/css/main.scss`:

- `.read-more`: `padding: 1rem; border: 1px solid;`
- `details, .toc`: `border: 1px solid; padding: 1rem;`
- Tables: full grid and header background.

## Consequences

- Do not replace these boxes with hairlines, left rules, or
  `--border-color` borders, and do not flag their brightness in dark mode.
- Do not propose the minimal table restyle again.
- Revisit only if Henry explicitly asks.
