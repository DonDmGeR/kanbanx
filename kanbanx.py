#!/usr/bin/env python3
"""
kanbanx.py 
Zero-Dependency, einzelne Datei, Windows-/Unix-Ready
Alle Daten werden im **selben Ordner wie das Skript** gespeichert.
"""
import argparse, json, uuid, datetime, sys
from pathlib import Path
import re

# ---------- Daten ----------
# Speichert alles im selben Verzeichnis wie das Skript
FILE = Path(__file__).with_suffix(".json")

def load():
    if not FILE.exists():
        return {"todo": [], "doing": [], "done": []}
    try:
        return json.loads(FILE.read_bytes().decode("utf-8"))
    except Exception:  # leere / defekte Datei
        return {"todo": [], "doing": [], "done": []}

def save(data):
    FILE.write_bytes(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

# ---------- Farben ----------
def colors(plain):
    if plain:
        return "", "", "", "", ""
    return ("\033[31m", "\033[32m", "\033[33m", "\033[36m", "\033[0m")

# ---------- Funktionen ----------
def add_task(args):
    data = load()
    content = " ".join(args.content_string) # Join all parts of the content string

    title = ""
    note = ""

    # Try to find a quoted title
    match = re.match(r'"(.*?)"\s*(.*)', content)
    if match:
        title = match.group(1)
        note = match.group(2).strip()
    else:
        # If no quoted title, take the first word as title, rest as note
        parts = content.split(maxsplit=1)
        title = parts[0]
        if len(parts) > 1:
            note = parts[1].strip()

    task = {
        "id": f"ID-{str(uuid.uuid4())[:6]}",  # 
        "title": title,
        "note": note,
        "subs": {},
        "clips": [],
        "created": str(datetime.datetime.now())
    }
    data[args.col].append(task)
    save(data)
    print(f"✅ '{title}' → {args.col} ({task['id']})")

def move_task(args):
    data = load()
    for col, tasks in data.items():
        for t in tasks:
            if t["id"] == args.id:
                tasks.remove(t)
                data[args.target].append(t)
                save(data)
                print(f"📦 {args.id} → {args.target}")
                return
    print("❌ ID nicht gefunden")

def add_sub(args):
    data = load()
    for col in data.values():
        for t in col:
            if t["id"] == args.id:
                sid = f"ID-{str(uuid.uuid4())[:6]}"  # 
                sub_text = " ".join(args.text) if isinstance(args.text, list) else args.text
                t["subs"][sid] = {"text": sub_text, "done": False}
                save(data)
                print(f"➕ Subtask {sid} zu {args.id}")
                return
    print("❌ Task nicht gefunden")

def done_sub(args):
    data = load()
    for col in data.values():
        for t in col:
            if t["id"] == args.id and args.subid in t["subs"]:
                t["subs"][args.subid]["done"] = True
                save(data)
                print(f"✅ {args.subid} erledigt")
                return
    print("❌ Subtask nicht gefunden")

def note_task(args):
    data = load()
    for col in data.values():
        for t in col:
            if t["id"] == args.id:
                note_text = " ".join(args.note) if isinstance(args.note, list) else args.note
                t["note"] += ("\n" + note_text).strip()
                save(data)
                print(f"📝 Notiz zu {args.id} gespeichert")
                return
    print("❌ Task nicht gefunden")


def clip_task(args):
    data = load()
    for col in data.values():
        for t in col:
            if t["id"] == args.id:
                snippet_text = " ".join(args.snippet) if isinstance(args.snippet, list) else args.snippet
                t["clips"].append({"ts": str(datetime.datetime.now()),
                                   "text": snippet_text})
                save(data)
                print(f"📎 Clip zu {args.id} gespeichert")
                return
    print("❌ Task nicht gefunden")

def list_tasks(args):
    data = load()
    RED, GREEN, YELLOW, CYAN, RESET = colors(args.plain)
    for col in ("todo", "doing", "done"):
        color = RED if col == "todo" else YELLOW if col == "doing" else GREEN
        print(f"\n{color}{col.upper()}{RESET}")
        for t in data[col]:
            print(f"  {CYAN}{t['id']}{RESET}  {t['title']}")
            if t["note"]:
                for line in t["note"].splitlines():
                    print(f"      {YELLOW}NOTE{RESET}  {line.strip()}")
            for sid, sub in t["subs"].items():
                mark = GREEN + "✓" + RESET if sub["done"] else RED + "○" + RESET
                print(f"        {mark} {sid}  {sub['text']}")
            for c in t["clips"][-3:]:
                print(f"      {CYAN}CLIP{RESET}  {c['text']}")

# ---------- Main ----------
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(
        description="KanbanX – Kanban + Task-Tree + Notes + Clipboard",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Beispiel:
  python kanbanx.py add todo "Release v2" "Epic: alles zusammenführen"
  python kanbanx.py sub ID-abc123 "Kapitel 1 schreiben"
  python kanbanx.py note ID-abc123 "Fokus auf Markdown"
  python kanbanx.py clip ID-abc123 "pip install rich"
  python kanbanx.py done ID-abc123 ID-def456
  python kanbanx.py move ID-abc123 done
  python kanbanx.py list
""")
    p.add_argument("--plain", action="store_true", help="Farben deaktivieren")
    sp = p.add_subparsers(dest="cmd")

    sp_add = sp.add_parser("add")
    sp_add.add_argument("col", choices=["todo", "doing", "done"])
    sp_add.add_argument("content_string", nargs=argparse.REMAINDER)

    sp_move = sp.add_parser("move")
    sp_move.add_argument("id")
    sp_move.add_argument("target", choices=["todo", "doing", "done"])

    sp_sub = sp.add_parser("sub")
    sp_sub.add_argument("id")
    sp_sub.add_argument("text", nargs=argparse.REMAINDER)

    sp_done = sp.add_parser("done")
    sp_done.add_argument("id")
    sp_done.add_argument("subid")

    sp_note = sp.add_parser("note")
    sp_note.add_argument("id")
    sp_note.add_argument("note", nargs=argparse.REMAINDER)

    sp_clip = sp.add_parser("clip")
    sp_clip.add_argument("id")
    sp_clip.add_argument("snippet", nargs=argparse.REMAINDER)

    sp_list = sp.add_parser("list")
    sp_list.add_argument("--plain", action="store_true")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return
    {
        "add": add_task,
        "move": move_task,
        "sub": add_sub,
        "done": done_sub,
        "note": note_task,
        "clip": clip_task,
        "list": list_tasks,
    }[args.cmd](args)

if __name__ == "__main__":
    main()