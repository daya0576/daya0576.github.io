---
name: new-post
description: Create a new Hugo blog post for zblog. Use when the user asks to create a new blog post or article. Handles slug generation, front matter, and file creation in the correct format.
---

# New Post

## Rules

- Post files use `.markdown` extension, **not** `.md`
- Posts live under `content/posts/`
- File path: `content/posts/<slug>.markdown` (single file, no subdirectory)
- Front matter format is YAML (delimited by `---`)
- `draft: true` by default unless the user says to publish

## Slug Rules

- Lowercase, hyphens only, no special characters
- Derived from the post title (translate Chinese to pinyin or English keywords if needed)
- Keep it concise (≤ 6 words)

## Front Matter Template

```yaml
---
title: "<exact title from user>"
date: <current datetime with timezone, e.g. 2026-03-11T20:00:00+08:00>
draft: true
series:
-
categories:
-
tags:
-
---
```

Only include `series` / `categories` / `tags` if the user provides them or they
can be inferred from similar posts (see below); otherwise omit those fields.

## Check Similar Posts

Before writing the front matter, check whether the post belongs to an existing
group (e.g. a recurring series like 派派成长日记). Look at sibling posts to stay
consistent:

- **series / categories**: `grep` existing posts in `content/posts/` for related
  files and reuse the same `series` and `categories` values verbatim. Example:
  `ls content/posts/ | grep -i <keyword>`, then inspect the front matter of the
  most recent match.
- **path / slug naming**: follow the naming pattern of the latest sibling post
  (e.g. `paipai-growth-diary-<N>-<keyword>`), not just an ad-hoc slug.
- **title numbering**: if the series uses a counter (e.g. `#15`), continue the
  sequence using the latest post as reference.

## Steps

1. Never ask for a title. If the user did not give one explicitly, derive it from
   whatever they provided (a URL, topic, pasted text) — fetch the page title if
   needed — and follow the naming style of the closest sibling post. Only if the
   input is truly ambiguous, proceed with the best guess and mention 1-2
   alternative titles in the final reply so the user can rename cheaply.
2. Check similar posts (see above) to infer `series` / `categories`, the slug
   naming pattern, and any title numbering.
3. Derive a slug from the title, matching the sibling naming pattern when the
   post belongs to an existing group.
4. Write `content/posts/<slug>.markdown` with the front matter above using the `write` tool.
5. Tell the user the full path of the created file.
6. Do **not** run `hugo new` — create the file directly with the `write` tool.
