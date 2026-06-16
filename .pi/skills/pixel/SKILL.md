---
name: pixel
description: Create a pixel/vintage blog header from a source image and update the matching blog post image URL.
---

# Pixel

Use this skill when the user gives a source image path/URL and wants the blog's pixel/vintage header style.

## Style

Create a progressive JPEG with:

- warm black-and-white / sepia tone
- film grain
- soft vignette
- subtle pixelation that preserves detail

## Workflow

1. Resolve the source image.
   - For a site URL like `/images/blog/global/foo.jpeg`, use `static/images/blog/global/foo.jpeg`.
   - For a bare filename, check the current directory, then `~/Downloads/`.
2. Pick a new output path under `static/images/blog/global/`, usually `SOURCE_STEM-pixel.jpg`. Never overwrite the source.
3. Ensure Pillow exists:

```bash
python3 -c "from PIL import Image; print('ok')"
```

If missing, ask before installing anything.

4. Generate the image:

```bash
python3 .pi/skills/pixel/scripts/vintage_header.py \
  "SOURCE_PATH" \
  "static/images/blog/global/OUTPUT.jpg"
```

5. Find the post that references the source image before asking the user:

```bash
grep -RIn "SOURCE_FILENAME\|/images/blog/global/SOURCE_FILENAME" content public --include='*.md' --include='*.markdown' --include='*.html'
```

If only `public/.../index.md` or `public/.../index.html` matches, infer the source post from the slug and find the matching file under `content/posts/`.

6. Replace the matching image reference in the content post with:

```markdown
![](/images/blog/global/OUTPUT.jpg)
```

If no matching post can be found, ask which post to update.

## Tuning

Default script settings are already tuned. For adjustments:

```bash
python3 .pi/skills/pixel/scripts/vintage_header.py input.jpg output.jpg \
  --pixel-scale 0.6 \
  --grain 10 \
  --vignette 0.6
```

- More detail: increase `--pixel-scale` toward `0.6` or `0.7`.
- More visible blocks: decrease `--pixel-scale` toward `0.35` or `0.25`.
- Less dirty: reduce `--grain` to `8` or `10`.
- Lighter edges: reduce `--vignette` to `0.5` or `0.6`.
