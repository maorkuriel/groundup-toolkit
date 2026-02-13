---
name: Google Workspace
description: Access Google Calendar, Gmail, and Google Docs/Drive using gog CLI. Download Google Docs, manage calendar events, and send emails.
---

# Google Workspace Integration

Use the `gog` CLI to interact with Google Calendar, Gmail, and Google Drive/Docs.

## Google Docs Operations

### Downloading Google Docs

To download a Google Doc as text:

```bash
~/.openclaw/skills/google-workspace/download-google-doc "DOCUMENT_URL_OR_ID"
```

**Examples:**
```bash
# Full URL
~/.openclaw/skills/google-workspace/download-google-doc "https://docs.google.com/document/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789_example/edit"

# Just the document ID
~/.openclaw/skills/google-workspace/download-google-doc "1aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789_example"
```

**When to use:**
- User shares a Google Docs link and asks you to process it
- User asks you to download or read a Google Doc
- User wants meeting notes from a Google Doc processed

**Important:** You CAN access Google Docs. Do NOT say you cannot access them.

Phone-to-email mappings are loaded from `config.yaml`. See `config.example.yaml` for format.

### Creating Calendar Events

**IMPORTANT:** The assistant has READ-ONLY access to team calendars. When creating events, create them on the assistant's calendar and invite the requesting user.

**Syntax for creating events:**

```bash
gog calendar create primary \
  --summary "Event Title" \
  --from "YYYY-MM-DDTHH:MM:SS+02:00" \
  --to "YYYY-MM-DDTHH:MM:SS+02:00" \
  --attendees user@yourcompany.com \
  --account your-assistant@yourcompany.com \
  --json
```

**Example: Create "Pick up kids from school" event:**

```bash
gog calendar create primary \
  --summary "Pick up kids from school" \
  --from "2026-02-08T12:45:00+02:00" \
  --to "2026-02-08T13:15:00+02:00" \
  --attendees user@yourcompany.com \
  --description "Reminder to pick up kids" \
  --account your-assistant@yourcompany.com \
  --json
```

**Time Format Guidelines:**
- Use RFC3339 format: `YYYY-MM-DDTHH:MM:SS+02:00`
- Israel timezone: `+02:00` (or `+03:00` during DST)
- For "today at 12:45", construct: `2026-02-08T12:45:00+02:00`
- Default duration: 30 minutes if not specified

**Optional Flags:**
- `--description "text"` - Add event description
- `--location "address"` - Add location
- `--reminder popup:15m` - Add 15-minute popup reminder
- `--with-meet` - Create Google Meet link
- `--all-day` - Make it an all-day event

### Important Notes:

1. **Always use --account with the assistant email** (from config) when creating events
2. **Always add the requesting user as --attendees**
3. **Use primary as the calendar ID** (assistant's calendar)
4. **Calculate proper timezone offset** (Israel is +02:00 or +03:00)
5. **If time is ambiguous**, ask the user for clarification

## Gmail Operations

### List emails:

```bash
gog gmail messages --max 10 --account your-assistant@yourcompany.com
```

### Search emails:

```bash
gog gmail messages --query "from:user@example.com" --max 5
```

### Read an email:

```bash
gog gmail thread <thread-id> --account your-assistant@yourcompany.com
```

## Authentication

All commands use the assistant account credentials (configured in config.yaml) stored in the gog keychain.

The GOG_KEYRING_PASSWORD environment variable is automatically set by the gateway service.
