# AGENTS.md

## Project Overview

This is a Hugo static blog published at https://changchen.me.

- Theme: `nostyleplease` as a Git submodule
- Hugo version: v0.154+
- Style direction: minimal

## Project Structure

```text
content/posts/       # Blog posts
content/about/       # About page
layouts/partials/    # Custom partials such as head.html and structured-data.html
layouts/shortcodes/  # Custom shortcodes such as video.html
layouts/footer.md    # Footer
static/images/       # Image assets
hugo.toml            # Site configuration
```

## Theme Notes

The `nostyleplease` theme is mounted as a Git submodule at `themes/nostyleplease`. Make theme changes directly inside the submodule when needed.

- CSS: `themes/nostyleplease/assets/css/main.scss`
- Keep all CSS in the SCSS file. Do not add inline styles in templates.
- Before adding styles, check for existing rules and keep the CSS DRY.
- Heading render hook: `layouts/_default/_markup/render-heading.html`
- Custom partial overrides: `layouts/partials/`
- Custom shortcodes: `layouts/shortcodes/`
- Theme partials: `themes/nostyleplease/layouts/partials/`

## Current Feature Work

- Rain Effect on the About page: see `docs/features/rain-effect.md`.

## API Catalog

- This site currently has no public API.
- Keep `static/.well-known/api-catalog` as an RFC 9727 linkset JSON document with an empty `linkset` array unless real APIs are added.
- Serve `/.well-known/api-catalog` as `application/linkset+json` via `static/_headers`.
- Do not invent `service-desc`, `service-doc`, or `status` links unless the corresponding API, documentation, and health endpoint exist.

## Important Guidance

- If an instruction is unclear or contradictory, ask a clarifying question or challenge it before implementing.
- Do not guess and implement ambiguous requirements silently.
