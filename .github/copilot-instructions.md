# GitHub Copilot Instructions for Henry Z's Blog

## Project Overview

This is a personal blog built with **Hugo** static site generator, using the **nostyleplease** theme. The blog focuses on technical content (SRE, Python, DevOps) and life topics (parenting, table tennis).

**Site URL**: https://changchen.me  
**Author**: Henry Zhu (daya0576)  
**Language**: Primarily Chinese (zh-hans) with some English content  
**Tech Stack**: Hugo, Go Templates, SCSS, Markdown

## Content Categories

### 1. 编程 (Programming)
- **Topics**: SRE, Python, DevOps, System Reliability, Open Source Projects
- **Examples**: 
  - Python internals and features (e.g., Dataclass, Python 3.14 highlights)
  - Self-hosted services and applications
  - Terminal tools and development workflows
  - Web accessibility and design

### 2. 生活 (Life)
- **Topics**: Parenting (派派成长日记), Book reviews, Personal reflections
- **Series**: "派派成长日记" (Paipai's Growth Diary) - parenting journey
- **Examples**:
  - Baby care tips and product recommendations
  - Parenting book reviews and notes
  - Personal growth and life reflections

### 3. Other Content
- Table tennis (YouTube videos)
- Tech tool recommendations
- Personal year-end summaries

## Code Style Guidelines

### Hugo Templates
- Use Go template syntax with Hugo-specific functions
- Prefer semantic HTML5 elements
- Follow existing indentation (2 spaces)
- Use Hugo's built-in functions: `absURL`, `relURL`, `humanize`, etc.
- Comment template logic with `{{- /* Comment */ -}}`

### Front Matter (Markdown)
```yaml
---
title: "文章标题"
description: "SEO 描述（可选）"
date: 2026-01-29T10:00:00+08:00
tags: ["tag1", "tag2"]
categories: ["编程"]  # or "生活"
series: ["series-name"]  # optional
images: ["/images/article-image.jpg"]  # optional but recommended for SEO
toc: true  # Table of Contents, default true
mathjax: false  # Enable if math equations needed
---
```

### CSS/SCSS
- Follow theme's existing style patterns
- Use semantic class names
- Maintain minimal, clean design philosophy
- Mobile-first responsive design

## SEO Best Practices

### Structured Data (JSON-LD)
- **Homepage**: WebSite, Person, Blog schemas
- **Articles**: BlogPosting schema with breadcrumbs
- **About Page**: AboutPage schema with Person entity
- **Archives**: CollectionPage schema
- Always include: `headline`, `datePublished`, `dateModified`, `author`, `description`
- Add `images` array when available (recommended 1200x630px)

### Meta Tags
- Always set canonical URL
- Include Open Graph tags for social sharing
- Add Twitter Cards
- Set proper `robots` and `googlebot` directives
- Include breadcrumb navigation

### Content Guidelines
- Write descriptive, SEO-friendly titles
- Add `description` in front matter (160 chars max)
- Use relevant tags and categories
- Include alt text for images
- Add internal links to related posts

## File Structure

```
/
├── archetypes/          # Content templates
├── content/
│   ├── about/          # About page
│   └── posts/          # All blog posts (.markdown)
├── layouts/
│   └── partials/       # Template partials
│       ├── head.html          # HTML head with SEO
│       ├── structured-data.html  # JSON-LD schemas
│       ├── footer.html
│       └── ...
├── static/             # Static files (images, robots.txt)
├── themes/
│   └── nostyleplease/ # Theme files
├── hugo.toml          # Hugo configuration
└── Makefile           # Build commands
```

## Writing Style

### Technical Posts
- Clear, concise explanations
- Include code examples with syntax highlighting
- Use headings for structure (H2, H3)
- Add images/diagrams when helpful
- Include "References" or "相关链接" section when needed

### Life Posts (Parenting)
- Personal, warm tone
- Share practical experiences and tips
- Include photos when relevant
- Reference books and resources
- Use emojis appropriately (👶, 😊, 🎉, etc.)

### Formatting
- Use inline code for commands/variables: `command`
- Use code blocks with language specifiers: ```python
- Use blockquotes for important notes: > Note
- Use lists for readability
- Bold important terms: **term**
- Add horizontal rules to separate sections: ---

## Hugo-Specific Guidelines

### URL Structure
- Posts: `/blog/YYYYMMDD/post-slug/`
- Archives: `/archives/`
- Categories: `/categories/category-name/`
- Tags: `/tags/tag-name/`
- Series: `/series/series-name/`

### Shortcodes
- Check `layouts/shortcodes/` for available custom shortcodes
- Use Hugo's built-in shortcodes when appropriate
- Prefer custom shortcodes for reusable content blocks

### Development Commands
```bash
# Start local server
hugo server -D

# Build production site
hugo

# Create new post
hugo new posts/YYYY-MM-DD-post-title.markdown
```

## Git Commit Guidelines

### Commit Message Format
```
<type>: <subject>

<body (optional)>
```

**Types**:
- `feat`: New feature or content
- `fix`: Bug fix
- `content`: Content updates or new posts
- `style`: CSS/design changes
- `seo`: SEO improvements
- `refactor`: Code restructuring
- `chore`: Maintenance tasks

**Examples**:
```
content: add new post about Python 3.14 features

feat: add CollectionPage schema for archives

seo: enhance structured data with breadcrumbs

fix: correct date format in article metadata
```

## Accessibility

- Use semantic HTML
- Provide alt text for all images
- Ensure proper heading hierarchy
- Maintain good color contrast
- Make links descriptive
- Support keyboard navigation

## Performance

- Optimize images before upload
- Use Hugo's asset pipeline for CSS/JS
- Enable fingerprinting for cache busting
- Minimize external dependencies
- Use lazy loading for images when possible

## Maintenance Notes

- Update Hugo version regularly
- Review and respond to Search Console issues
- Monitor site performance with PageSpeed Insights
- Keep theme and dependencies up to date
- Back up content regularly

## Special Considerations

### Chinese Content
- Use proper Chinese punctuation (，。！？)
- Prefer Chinese quotes: 「」or ""
- Mix English terms naturally when needed
- Maintain readability for Chinese readers

### Multilingual Support
- Primary language: Chinese (zh-hans)
- Some technical terms remain in English
- Code and technical content may be bilingual
- Maintain consistent language within each post

## Resources

- Hugo Documentation: https://gohugo.io/documentation/
- Schema.org: https://schema.org/
- Google Search Central: https://developers.google.com/search
- Author's GitHub: https://github.com/daya0576
