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
categories:
-
tags:
-
---
```

Only include `categories` / `tags` if the user provides them; otherwise omit those fields.

## Steps

1. If the user has not provided a title, ask: "文章标题是什么？" and wait for the answer before proceeding.
2. Derive a slug from the title.
3. Write `content/posts/<slug>.markdown` with the front matter above using the `write` tool.
4. Tell the user the full path of the created file.
5. Do **not** run `hugo new` — create the file directly with the `write` tool.
