---
name: content-writer
description: Generate content (LinkedIn posts, Substack notes, newsletters) in Navot's voice via WhatsApp. Uses voice DNA, audience profiles, and business context for authentic content.
version: 1.0.0
author: GroundUp VC
actions:
  - generate
  - test
---

# Content Writer

Generate written content in Navot's authentic voice — LinkedIn posts, Substack notes, and thought leadership newsletters. Uses comprehensive voice DNA, audience profiles, and business context to produce content that sounds like Navot, not like generic AI.

## When to Use This Skill

**WhatsApp triggers (from team members):**
- "write a LinkedIn post about [topic]"
- "draft a post about [topic]"
- "write a substack note about [topic]"
- "write a note about [topic]"
- "write a newsletter about [topic]"
- "write an article about [topic]"
- "write about [topic]" (defaults to LinkedIn post)
- Hebrew messages work too — output will be in Hebrew with English tech terms

## Content Types

### LinkedIn Post
Short-form content (150-300 words). Direct, insight-driven, observation-first.
Delivered via WhatsApp.

### Substack Note
Ultra-short content (1-10 sentences). Punchy, quotable, single-insight format.
Delivered via WhatsApp.

### Newsletter / Article
Long-form thought leadership (800-1500 words). Includes subject line options, sectioned headers, skim-optimized.
Delivered via WhatsApp preview + full version by email.

## Actions

### generate

Generate content from a WhatsApp message.

```bash
content-writer generate "<message>" "<sender-phone>"
```

### test

Run a test generation (sends a LinkedIn post to the alert phone).

```bash
content-writer test
```

## Configuration

Uses shared `config.yaml` and `.env` — no additional configuration needed.

Required environment variables:
- `ANTHROPIC_API_KEY` — Claude AI for content generation
