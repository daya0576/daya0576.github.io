#!/usr/bin/env python3
"""Create a black-and-white vintage zblog header image."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps


def tone_grayscale(gray: Image.Image, shadow: tuple[int, int, int], highlight: tuple[int, int, int]) -> Image.Image:
    lut_r: list[int] = []
    lut_g: list[int] = []
    lut_b: list[int] = []
    for i in range(256):
        t = i / 255
        lut_r.append(int(shadow[0] + (highlight[0] - shadow[0]) * t))
        lut_g.append(int(shadow[1] + (highlight[1] - shadow[1]) * t))
        lut_b.append(int(shadow[2] + (highlight[2] - shadow[2]) * t))
    return Image.merge("RGB", (gray.point(lut_r), gray.point(lut_g), gray.point(lut_b)))


def add_grain(img: Image.Image, amount: float, blend: float) -> Image.Image:
    noise = Image.effect_noise(img.size, amount).convert("L")
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    grainy = ImageChops.add(img, noise_rgb, scale=2.0, offset=-32)
    return Image.blend(img, grainy, blend)


def add_vignette(img: Image.Image, strength: float) -> Image.Image:
    width, height = img.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    pad_x, pad_y = int(width * 0.05), int(height * 0.05)
    draw.ellipse([pad_x, pad_y, width - pad_x, height - pad_y], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=min(width, height) / 4))
    dark = Image.new("RGB", (width, height), (0, 0, 0))
    vignetted = Image.composite(img, dark, mask)
    return Image.blend(img, vignetted, strength)


def pixelate(img: Image.Image, scale: float) -> Image.Image:
    if scale >= 1:
        return img
    width, height = img.size
    small = img.resize((max(1, int(width * scale)), max(1, int(height * scale))), Image.NEAREST)
    return small.resize((width, height), Image.NEAREST)


def process(args: argparse.Namespace) -> None:
    src = Path(args.source).expanduser()
    dst = Path(args.output).expanduser()

    img = Image.open(src).convert("RGB")

    if img.width > args.max_width:
        new_height = int(img.height * args.max_width / img.width)
        img = img.resize((args.max_width, new_height), Image.LANCZOS)

    gray = ImageOps.grayscale(img)
    gray = ImageOps.autocontrast(gray, cutoff=args.autocontrast_cutoff)
    gray = ImageEnhance.Contrast(gray).enhance(args.contrast)
    gray = ImageEnhance.Brightness(gray).enhance(args.brightness)

    img = tone_grayscale(gray, args.shadow, args.highlight)
    img = add_grain(img, amount=args.grain, blend=args.grain_blend)
    img = add_vignette(img, strength=args.vignette)
    img = pixelate(img, scale=args.pixel_scale)

    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "JPEG", quality=args.quality, optimize=True, progressive=True)
    print(f"saved: {dst} {img.size} {os.path.getsize(dst)} bytes")


def rgb(value: str) -> tuple[int, int, int]:
    parts = tuple(int(part.strip()) for part in value.split(","))
    if len(parts) != 3 or any(part < 0 or part > 255 for part in parts):
        raise argparse.ArgumentTypeError("expected R,G,B values in 0..255")
    return parts  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="source image path")
    parser.add_argument("output", help="output JPEG path")
    parser.add_argument("--max-width", type=int, default=1600)
    parser.add_argument("--autocontrast-cutoff", type=float, default=2)
    parser.add_argument("--contrast", type=float, default=1.18)
    parser.add_argument("--brightness", type=float, default=0.96)
    parser.add_argument("--shadow", type=rgb, default=(38, 28, 20), help="shadow tone as R,G,B")
    parser.add_argument("--highlight", type=rgb, default=(244, 232, 208), help="highlight tone as R,G,B")
    parser.add_argument("--grain", type=float, default=14)
    parser.add_argument("--grain-blend", type=float, default=0.35)
    parser.add_argument("--vignette", type=float, default=0.7)
    parser.add_argument("--pixel-scale", type=float, default=0.5)
    parser.add_argument("--quality", type=int, default=92)
    process(parser.parse_args())


if __name__ == "__main__":
    main()
