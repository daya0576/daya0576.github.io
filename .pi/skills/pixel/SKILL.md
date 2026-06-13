---
name: pixel
description: Create a pixel/vintage blog header from a source image and update the blog post image URL. Use when the user provides a source image path and asks for the pixel/vintage header style.
---

# Pixel

Use this skill when the input is a source image path, for example `xxx.jpg` or `/path/to/xxx.png`. The expected workflow is: create a new processed header image, then update the target blog post to reference the new image URL.

## Style

Target look:

- Blog header image suitable for the minimal `nostyleplease` theme
- Black-and-white vintage base
- Warm brown / selenium-style toning
- Film grain
- Soft vignette
- Subtle pixelation while preserving details
- Progressive JPEG output

Canonical prompt summary:

> Process the image as a minimal-blog header with black-and-white vintage styling: warm sepia/selenium monochrome, film grain, soft vignette, and subtle pixelation that preserves detail. Output as a progressive JPEG.

## Default Parameters

These are the final tuned values from the previous session:

- max width: `1600`
- autocontrast cutoff: `2`
- contrast: `1.18`
- brightness: `0.96`
- warm tone shadow: `(38, 28, 20)`
- warm tone highlight: `(244, 232, 208)`
- grain amount: `14`
- grain blend: `0.35`
- vignette strength: `0.7`
- pixel scale: `0.5`
- JPEG quality: `92`

## Input

The user input should be treated as the **source image** path, for example:

```text
xxx.jpg
/path/to/xxx.png
```

If the target blog post is not obvious from the user's request or current context, ask which post to update before editing content.

## Workflow

1. Resolve the source image path. If the user gives a bare filename such as `xxx.jpg`, check the current directory first, then common locations such as `~/Downloads/`.
2. Choose a **new** output path under `static/images/blog/global/`. Do not overwrite the source image. Prefer a short unique name based on the source stem or timestamp, e.g. `static/images/blog/global/xxx-pixel.jpg`.
3. Run the helper script:

```bash
python3 .pi/skills/pixel/scripts/vintage_header.py \
  "/path/to/source.jpg" \
  "static/images/blog/global/output-name.jpg"
```

4. Update the target blog post image URL to reference the new image:

```markdown
![](/images/blog/global/output-name.jpg)
```

Usually this means replacing the first header image near the top of the post. If no header image exists, insert this Markdown image immediately after front matter.

5. Preview if requested:

```bash
open static/images/blog/global/output-name.jpg
```

## Tuning

Use these options when the user asks for adjustments:

```bash
python3 .pi/skills/pixel/scripts/vintage_header.py \
  input.jpg output.jpg \
  --pixel-scale 0.6 \
  --grain 10 \
  --vignette 0.6
```

Guidance:

- More subtle pixelation / more detail: increase `--pixel-scale` toward `0.6` or `0.7`.
- More visible pixel blocks: decrease `--pixel-scale` toward `0.35` or `0.25`.
- Too dirty: reduce `--grain` to `8` or `10`.
- Too dark at edges: reduce `--vignette` to `0.5` or `0.6`.
- More contrast: increase `--contrast` to `1.25`.

## Requirements

The script uses Pillow. Check availability with:

```bash
python3 -c "from PIL import Image; print('ok')"
```

If Pillow is missing, ask before installing dependencies.
