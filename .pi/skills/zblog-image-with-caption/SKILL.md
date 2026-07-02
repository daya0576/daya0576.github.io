---
name: zblog-image-with-caption
description: Insert or explain an image with caption in zblog posts. Use when the user asks to add an image caption, image footer, figure, or asks for the zblog image caption syntax.
---

# zblog Image With Caption

Use Hugo's built-in `figure` shortcode for images that need a visible caption/footer.

## Syntax

```markdown
{{< figure src="/images/blog/<path>/<file>" alt="<accessible description>" caption="<caption shown under the image>" >}}
```

## Rules

- Store post images under `static/images/`, usually `static/images/blog/...`.
- Reference static assets with a leading slash, e.g. `/images/blog/global/example.jpg`.
- Always provide meaningful `alt` text unless the image is purely decorative.
- Use `caption` for the text shown below the image.
- Do not add inline HTML or inline styles for normal captioned images.
- To find which post an image belongs in, grep `content/posts/` for the image filename instead of asking the user.
- For an uncaptained image, Markdown is acceptable:

```markdown
![alt text](/images/blog/<path>/<file>)
```

## Example

```markdown
{{< figure src="/images/blog/global/BBE85036-8B31-4AAE-A309-0EC0B1836DD3_1_201_a.jpeg" alt="Pai holding a toy and interacting with a classmate" caption="Pai is on the right, holding a toy and interacting with a classmate." >}}
```
