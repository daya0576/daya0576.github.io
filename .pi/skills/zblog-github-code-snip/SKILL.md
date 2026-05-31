---
name: zblog-github-code-snip
description: Insert or explain a GitHub code snippet reference in zblog posts. Use when the user asks to quote GitHub source code, add a GitHub code block, or asks for the zblog GitHub code snippet syntax.
---

# zblog GitHub Code Snippet

Use this skill for Hugo posts in this repository when referencing source code from GitHub.

## Syntax

Place the custom shortcode immediately before a normal fenced code block. When replying to the user, output the snippet directly so it can be copied and pasted; do not wrap the whole answer in an outer Markdown code fence.

{{< github-code url="https://github.com/<owner>/<repo>/blob/<commit-or-branch>/<path>#L<start>-L<end>" >}}

```<language>
<code copied from GitHub>
```

## Rules

- Use `layouts/shortcodes/github-code.html`; the shortcode only renders the GitHub source link/header.
- Always include the code manually in the fenced block after the shortcode; the shortcode does not fetch or embed code content.
- Prefer a permalink with a commit SHA instead of a moving branch when quoting code for long-term accuracy.
- Include line fragments when available, e.g. `#L147-L164` or `#L87`.
- Match the fence language to the code (`ts`, `py`, `go`, `sh`, etc.).
- Keep the shortcode and the code block adjacent, separated by at most one blank line.

## Example

{{< github-code url="https://github.com/badlogic/pi-mono/blob/380236a003ec7f0e69f54463b0f00b3118d78f3c/packages/coding-agent/src/core/system-prompt.ts#L147-L164" >}}

```ts
let prompt = `You are an expert coding assistant operating inside pi...`;
```
