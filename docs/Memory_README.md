# How Claude Code Memory Works in This Project

> Understanding the persistent memory system that maintains context across sessions.

---

## Two Persistence Mechanisms

### Project-level: `CLAUDE.md` (in your project root)
- Lives at `/FLUENT_PYTHON/CLAUDE.md`
- **Checked into git** — shared with collaborators
- Auto-loaded every session in that directory
- Contains project instructions, coding standards, architecture
- You created and control this file

### Global: `~/.claude/projects/.../memory/` (hidden, outside project)
- Lives at `~/.claude/projects/<hashed-path>/memory/`
- **Not in git** — private to your machine
- Contains personal context: your preferences, feedback corrections, external references
- Managed by Claude Code automatically
- Scoped by working directory path (the long hash in the folder name maps to your project path)

### Why the separation matters

| Concern | CLAUDE.md | ~/.claude/memory/ |
|---------|-----------|-------------------|
| **Who sees it?** | Anyone with repo access | Only you |
| **What goes in it?** | Project facts, standards | Personal preferences, corrections, references |
| **Git tracked?** | Yes | No |
| **Example** | "Use pytest, not unittest" | "User is a clinical informaticist, prefers terse responses" |
| **Survives repo clone?** | Yes | No (machine-local) |

---

## The 3 Memory Files

### File 1: `MEMORY.md` — The Index

```
# Memory Index
## Project
- clinicalnlp decisions → project_clinicalnlp_decisions.md
## Reference
- Fluent Python PDF → reference_fluent_python_pdf.md
```

**What it does:** This is the **table of contents**. It's loaded into every new conversation automatically. It contains no content itself — just pointers to the actual memory files. This keeps it small (max 200 lines) so it doesn't waste context window space.

**How it's used:** When Claude starts a new session, it sees this index and knows what memories exist. If the current task is relevant to one of these pointers, it reads the full memory file.

---

### File 2: `project_clinicalnlp_decisions.md` — Curriculum Decisions

The frontmatter tells Claude when to use it:
- **`type: project`** — this is about ongoing project state
- **`description:`** — matched against the current task to decide relevance

The body records the 7 resolved decisions plus **Why** (motivation) and **How to apply** (concrete rules to follow).

**How it's used in future sessions:**
- When you say "let's start Module 3" → Claude reads this and knows: use `.py` scripts, one concept per session, update docs alongside code, use offline data (not real FHIR yet)
- Prevents re-asking questions you already answered
- The "How to apply" line means every session produces: code + test update + doc update

---

### File 3: `reference_fluent_python_pdf.md` — Book Location & Page Map

**How it's used in future sessions:**
- When deep-diving Module 1 and Claude needs to reference what Ramalho says about `__repr__` → it knows to read pages 21-55 of the PDF
- When you ask "what does the book say about generators?" → Claude knows Part IV starts at Chapter 17 and can read the right pages
- The companion code path means Claude can cross-reference `example-code-2e/01-data-model/` while building the clinical version

---

## How They Work Together in a Session

```
New conversation starts
        |
MEMORY.md auto-loaded (index only)
        |
You say: "Let's implement __repr__ for PatientRecord"
        |
Claude checks index → relevant: both memories
        |
Read decisions → one concept per session, .py scripts, update docs
Read PDF ref → Chapter 1, pages 21-55, example-code-2e/01-data-model/
        |
Claude also reads CLAUDE.md (project root) for coding standards
        |
Now Claude has full context without you repeating anything
```

---

## What Gets Added Over Time

As we work through modules, this memory system grows:

| Type | Example | When |
|------|---------|------|
| **feedback** | "Don't explain things I already know about FHIR" | When you correct Claude's behavior |
| **user** | "Prefers seeing memory diagrams for data structures" | When Claude learns your learning style |
| **project** | "Module 1 completed on 2026-03-20" | When a module is finished |
| **reference** | "HAPI FHIR test server URL for Module 5" | When external resources are set up |

This way, session 15 has the same context quality as session 1 — no "amnesia" between conversations.

---

## Memory File Location

```
~/.claude/projects/<hashed-project-path>/memory/
├── MEMORY.md                          ← Index (auto-loaded)
├── project_clinicalnlp_decisions.md   ← Curriculum decisions
└── reference_fluent_python_pdf.md     ← Book PDF location & page map
```

Note: The `.claude` folder is **hidden** (starts with a dot).
- **VS Code:** `Cmd + Shift + P` → "Open File" → paste the path
- **Finder:** `Cmd + Shift + .` to toggle hidden files
- **Terminal:** `ls -la ~/.claude/projects/`
