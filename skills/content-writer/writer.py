#!/usr/bin/env python3
"""
Content Writer — WhatsApp-triggered content generation in Navot's voice.

Usage:
  python3 writer.py generate "<message>" "<sender-phone>"
  python3 writer.py test
"""

import sys
import os
import re
import json
import subprocess
import tempfile
import requests

# Load shared config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from lib.config import config

# --- Constants ---

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONTEXT_DIR = os.path.join(SKILL_DIR, 'context')
ANTHROPIC_API_KEY = config.anthropic_api_key
GOG_ACCOUNT = config.assistant_email

# Content type definitions
CONTENT_TYPES = {
    'linkedin_post': {
        'label': 'LinkedIn Post',
        'patterns': [
            r'linkedin\s+post', r'linkedin\s+content', r'post\s+(about|on)\b',
            r'write\s+a\s+post', r'thread\s+(about|on)\b', r'social\s+post',
        ],
        'max_whatsapp': 3800,
        'send_email': False,
    },
    'substack_note': {
        'label': 'Substack Note',
        'patterns': [
            r'substack\s+note', r'write\s+a\s+note', r'short\s+note',
            r'quick\s+note', r'note\s+(about|on)\b',
        ],
        'max_whatsapp': 3800,
        'send_email': False,
    },
    'newsletter': {
        'label': 'Newsletter / Article',
        'patterns': [
            r'newsletter', r'\barticle\b', r'thought\s+leadership',
            r'long\s*form', r'substack\s+post', r'essay',
        ],
        'max_whatsapp': 3800,
        'send_email': True,
    },
}

WEEKLYSYNC_KEYWORDS = [
    'weekly sync', 'weeklysync', 'podcast', 'episode',
    'kitchen conversation', 'tech news', 'hebrew content',
    'show notes', 'episode recap',
]


# --- Profile Loading ---

def load_json_profile(filename):
    path = os.path.join(CONTEXT_DIR, filename)
    with open(path) as f:
        return json.load(f)


def condense_voice_dna(data):
    """Extract essential English voice characteristics."""
    vd = data.get('data', {}).get('voice_dna', {})
    cs = data.get('data', {}).get('communication_style', {})
    lf = data.get('data', {}).get('linguistic_fingerprint', {})
    vb = data.get('data', {}).get('voice_boundaries', {})

    parts = []
    parts.append(f"CORE ESSENCE: {vd.get('core_essence', {}).get('en', '')}")
    parts.append(f"WORLDVIEW: {vd.get('worldview', {}).get('en', '')}")
    parts.append(f"EMOTIONAL PALETTE: {', '.join(vd.get('emotional_palette', []))}")
    parts.append(f"SOCIAL POSITIONING: {vd.get('social_positioning', {}).get('en', '')}")
    parts.append(f"THOUGHT PROGRESSION: {cs.get('thought_progression', {}).get('en', '')}")
    parts.append(f"COMPLEXITY: {cs.get('complexity_preference', {}).get('en', '')}")

    # Conviction spectrum
    conv = cs.get('conviction_spectrum', {})
    parts.append(f"CONVICTION: {conv.get('typical_balance', {}).get('en', '')}")

    # Sentence patterns
    sp = lf.get('sentence_architecture', {}).get('typical_patterns', [])
    if sp:
        parts.append(f"SENTENCE PATTERNS: {'; '.join(sp[:6])}")

    # Signature colloquialisms
    colloquialisms = lf.get('vocabulary_tendencies', {}).get('signature_colloquialisms', [])
    if colloquialisms:
        parts.append(f"SIGNATURE PHRASES: {'; '.join(colloquialisms[:8])}")

    # Code switching
    code_switch = lf.get('code_switching', {})
    if code_switch:
        he_en = code_switch.get('hebrew_english_patterns', {}).get('en', '')
        if he_en:
            parts.append(f"CODE-SWITCHING: {he_en}")

    # Voice boundaries
    if vb:
        never = vb.get('never_sounds_like', [])
        always = vb.get('always_sounds_like', [])
        if never:
            parts.append(f"NEVER SOUNDS LIKE: {'; '.join(never[:6])}")
        if always:
            parts.append(f"ALWAYS SOUNDS LIKE: {'; '.join(always[:6])}")

    return '\n'.join(parts)


def condense_icp(data):
    """Extract key audience info for newsletter system prompt."""
    icp = data.get('data', {})
    parts = []

    identity = icp.get('identity', {})
    if identity.get('description_english'):
        parts.append(f"AUDIENCE: {identity['description_english']}")

    pain = icp.get('pain_points', {})
    primary = pain.get('primary_problem_english', '')
    if primary:
        parts.append(f"PRIMARY PROBLEM: {primary}")
    secondary = pain.get('secondary_problems_english', [])
    if secondary:
        parts.append(f"OTHER PROBLEMS: {'; '.join(secondary[:5])}")

    aspirations = icp.get('aspirations', {})
    dream = aspirations.get('dream_outcome_english', '')
    if dream:
        parts.append(f"DREAM OUTCOME: {dream}")

    lang = icp.get('language_patterns', {})
    problem_lang = lang.get('problem_language', [])
    if problem_lang:
        parts.append(f"HOW THEY TALK: {'; '.join(problem_lang[:5])}")

    return '\n'.join(parts)


def select_business_profile(message):
    msg_lower = message.lower()
    for kw in WEEKLYSYNC_KEYWORDS:
        if kw in msg_lower:
            return load_json_profile('business-weeklysync.json')
    return load_json_profile('business-groundup.json')


def format_business_profile(data):
    """Format business profile as readable text."""
    bp = data.get('data', {})
    parts = []

    basic = bp.get('basic_info', {})
    if basic:
        parts.append(f"BUSINESS: {basic.get('name', '')} — {basic.get('tagline_english', basic.get('tagline', ''))}")

    positioning = bp.get('positioning', {})
    if positioning:
        angle = positioning.get('unique_angle_english', positioning.get('unique_angle', ''))
        if angle:
            parts.append(f"POSITIONING: {angle}")
        philosophy = positioning.get('core_philosophy_english', positioning.get('core_philosophy', ''))
        if philosophy:
            parts.append(f"PHILOSOPHY: {philosophy}")

    differentiators = bp.get('differentiators', [])
    if differentiators:
        diff_texts = []
        for d in differentiators[:5]:
            if isinstance(d, dict):
                diff_texts.append(d.get('english', d.get('hebrew', str(d))))
            else:
                diff_texts.append(str(d))
        parts.append(f"DIFFERENTIATORS: {'; '.join(diff_texts)}")

    tone = bp.get('tone', {})
    if tone:
        attrs = tone.get('attributes', tone.get('attributes_english', []))
        if attrs:
            parts.append(f"TONE: {'; '.join(attrs[:6])}")

    return '\n'.join(parts)


# --- Content Type Detection ---

def detect_content_type(message):
    msg_lower = message.lower()
    for ctype, info in CONTENT_TYPES.items():
        for pattern in info['patterns']:
            if re.search(pattern, msg_lower):
                return ctype

    # Fallback: use Haiku to classify
    return classify_with_haiku(message)


def classify_with_haiku(message):
    prompt = f"""Classify this content request into exactly one type.

REQUEST: "{message}"

Types:
- linkedin_post (short post, social media, thread)
- substack_note (short note, quick thought, 1-10 sentences)
- newsletter (long article, newsletter, essay, thought leadership)

Reply with ONLY the type name, nothing else."""

    try:
        result = call_claude(prompt, model="claude-haiku-4-5-20251001", max_tokens=20)
        result = result.strip().lower().replace('"', '').replace("'", "")
        if result in CONTENT_TYPES:
            return result
    except Exception:
        pass
    return 'linkedin_post'  # safe default


# --- System Prompt Assembly ---

def detect_hebrew(message):
    return bool(re.search(r'[\u0590-\u05FF]', message))


def build_system_prompt(content_type, business_profile_data, message, include_icp=False):
    voice_data = load_json_profile('voice-dna.json')
    voice = condense_voice_dna(voice_data)
    business = format_business_profile(business_profile_data)

    is_hebrew = detect_hebrew(message)

    parts = [
        "You are a content writer for Navot, an Israeli tech founder and VC at GroundUp Ventures.",
        "",
        "VOICE PROFILE:",
        voice,
        "",
        "BUSINESS CONTEXT:",
        business,
        "",
    ]

    if is_hebrew:
        parts.extend([
            "LANGUAGE: Write in Hebrew. Use English tech terms naturally (AI, ROI, startup, founder, etc.) as described in the voice profile's code-switching patterns.",
            "",
        ])
    else:
        parts.extend([
            "LANGUAGE: Write in English. Maintain the Israeli-direct-skeptical voice. Occasional Hebrew terms are fine when they add flavor.",
            "",
        ])

    # Content-type-specific instructions
    if content_type == 'linkedin_post':
        parts.extend([
            "CONTENT TYPE: LinkedIn Post",
            "- Length: 150-300 words (1000-2000 characters)",
            "- Structure: Hook line → observation/insight → pattern → conclusion",
            "- Short paragraphs with line breaks between them",
            "- NO hashtags unless specifically requested",
            "- NO emojis unless specifically requested",
            "- End with an insight, not a call-to-action",
            "- Write ONLY the post content, no meta-commentary",
        ])
    elif content_type == 'substack_note':
        parts.extend([
            "CONTENT TYPE: Substack Note",
            "- Length: 1-10 sentences (50-500 words)",
            "- Choose the best format: single-punch wisdom, pattern observation, contrarian statement, or direct advice",
            "- Be punchy. Every word earns its place.",
            "- Can be a single powerful line or a short developed thought",
            "- Write ONLY the note content, no meta-commentary",
        ])
    elif content_type == 'newsletter':
        parts.extend([
            "CONTENT TYPE: Thought Leadership Newsletter",
            "- Length: 800-1500 words",
            "- Start with 3 subject line options (each on its own line, prefixed with 'Subject: ')",
            "- Then a blank line, then the full newsletter",
            "- Structure: Hook introduction → 3-7 sections with standalone-value headers → closing",
            "- Headers should be full sentences that deliver value on their own",
            "- Each section: opener → development → closer (1-3 sentences each)",
            "- Skim-optimized: someone reading just the headers gets 80% of the value",
            "- Short paragraphs (1-3 sentences max), generous white space",
        ])
        if include_icp:
            icp_data = load_json_profile('icp.json')
            icp = condense_icp(icp_data)
            parts.extend(["", "AUDIENCE CONTEXT:", icp])

    parts.extend([
        "",
        "CRITICAL RULES:",
        "- Sound like Navot, not like generic AI. Refer to the voice boundaries above.",
        "- No corporate speak, no hype language, no management consultant tone.",
        "- Be direct, skeptical, pattern-observing. Not preachy.",
        "- Concrete observations before abstract insights.",
        "- Short paragraphs. Breathing room.",
    ])

    return '\n'.join(parts)


# --- Claude API ---

def call_claude(prompt, system_prompt="", model="claude-sonnet-4-20250514", max_tokens=4096):
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }
    if system_prompt:
        payload["system"] = system_prompt

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json=payload,
        timeout=90
    )
    if response.status_code != 200:
        print(f"Claude API error: {response.status_code} {response.text[:200]}", file=sys.stderr)
        return "Content generation failed — API error."
    return response.json()["content"][0]["text"]


# --- Delivery ---

def send_whatsapp(phone, message, max_retries=3, retry_delay=3):
    import time
    for attempt in range(1, max_retries + 1):
        try:
            cmd = [
                'openclaw', 'message', 'send',
                '--channel', 'whatsapp',
                '--target', phone,
                '--message', message
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                print(f"  ✓ WhatsApp sent to {phone}" + (f" (attempt {attempt})" if attempt > 1 else ""))
                return True
            else:
                print(f"  ✗ Attempt {attempt}/{max_retries}: {result.stderr.strip()[:100]}", file=sys.stderr)
                if attempt < max_retries:
                    time.sleep(retry_delay)
        except Exception as e:
            print(f"  ✗ Attempt {attempt}/{max_retries}: {e}", file=sys.stderr)
            if attempt < max_retries:
                time.sleep(retry_delay)
    return False


def send_email(to_email, subject, body):
    try:
        body_file = tempfile.mktemp(suffix='.txt')
        with open(body_file, 'w') as f:
            f.write(body)

        cmd = [
            'gog', 'gmail', 'send',
            '--to', to_email,
            '--subject', subject,
            '--body-file', body_file,
            '--account', GOG_ACCOUNT,
            '--force', '--no-input'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        try:
            os.unlink(body_file)
        except Exception:
            pass

        if result.returncode == 0:
            print(f"  ✓ Email sent to {to_email}")
            return True
        else:
            print(f"  ✗ Email failed: {result.stderr.strip()[:200]}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"  ✗ Email exception: {e}", file=sys.stderr)
        return False


def split_for_whatsapp(text, max_chars=3800):
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current = ""
    paragraphs = text.split('\n\n')

    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars:
            if current:
                chunks.append(current.strip())
                current = para + '\n\n'
            else:
                # Single paragraph exceeds limit — force split
                while len(para) > max_chars:
                    cut = para[:max_chars].rfind('. ')
                    if cut < 100:
                        cut = max_chars
                    chunks.append(para[:cut + 1].strip())
                    para = para[cut + 1:].strip()
                current = para + '\n\n'
        else:
            current += para + '\n\n'

    if current.strip():
        chunks.append(current.strip())

    if len(chunks) > 1:
        total = len(chunks)
        chunks = [f"[{i+1}/{total}]\n\n{chunk}" for i, chunk in enumerate(chunks)]

    return chunks


def deliver_content(content, content_type, phone, email=None):
    ct = CONTENT_TYPES[content_type]

    if ct['send_email'] and email:
        # Newsletter: extract subject line and send full via email
        subject = "Draft: Content from Christina"
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('Subject:'):
                subject = line.strip().replace('Subject:', '').strip()
                break

        send_email(email, subject, content)

        # WhatsApp: preview + pointer to email
        preview = content[:3500]
        if len(content) > 3500:
            preview += "\n\n---\n[Full version sent to your email]"
        send_whatsapp(phone, preview)
    else:
        # Short content: send directly via WhatsApp
        chunks = split_for_whatsapp(content)
        for chunk in chunks:
            send_whatsapp(phone, chunk)


# --- Main ---

def generate(message, sender_phone):
    print(f"Content request from {sender_phone}: {message[:80]}...")

    # Look up sender for email delivery
    member = config.get_member_by_phone(sender_phone)
    sender_email = member['email'] if member else None

    # Detect content type
    content_type = detect_content_type(message)
    ct_label = CONTENT_TYPES[content_type]['label']
    print(f"  Content type: {ct_label}")

    # For newsletters, send acknowledgment
    if content_type == 'newsletter':
        send_whatsapp(sender_phone, f"Working on your {ct_label.lower()}, this will take about 30 seconds...")

    # Select business profile
    business_profile = select_business_profile(message)

    # Build system prompt
    system_prompt = build_system_prompt(
        content_type, business_profile, message,
        include_icp=(content_type == 'newsletter')
    )

    # Generate content
    user_prompt = f"Write a {ct_label.lower()} based on this request:\n\n{message}"
    content = call_claude(user_prompt, system_prompt)

    # Deliver
    deliver_content(content, content_type, sender_phone, sender_email)
    print(f"  ✓ {ct_label} delivered")


def test():
    phone = config.alert_phone
    print(f"Running test — sending LinkedIn post to {phone}")
    generate("Write a LinkedIn post about why most VC content is boring and what founders actually want to read", phone)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]

    if action == 'generate':
        if len(sys.argv) < 4:
            print("Usage: writer.py generate <message> <sender-phone>")
            sys.exit(1)
        generate(sys.argv[2], sys.argv[3])

    elif action == 'test':
        test()

    else:
        print(f"Unknown action: {action}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
