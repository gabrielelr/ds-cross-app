#!/usr/bin/env python3
"""
DS Screen Scorer — v1

Confronta una schermata (rappresentata come JSON neutro) contro il page-pattern
corrispondente e produce un report pass/fail per ogni slot / regola / anti-pattern.

Input JSON neutro:
{
  "pageType": "detail-product-game",      # slug del page-pattern
  "slots": {                              # mapping slot-name -> [componenti presenti]
    "statusBar": ["Status Bar OS"],
    "hero": ["Hero Detail"],
    "characteristics": ["Card Detail"],
    "stickyFooter": ["Button Group"]
  },
  "componentsUsed": [                     # lista flat di TUTTI i componenti (per check globali)
    {"slug": "button", "props": {"hierarchy": "primary"}},
    {"slug": "button", "props": {"hierarchy": "secondary"}},
    {"slug": "hero-detail", "props": {}},
    {"slug": "card-detail", "props": {}}
  ]
}

Exit code: 0 se conforme, 1 se ci sono violazioni.

V1 limitazioni:
- pageType deve essere dichiarato esplicitamente (no auto-detect)
- antiPatterns vengono elencati ma non verificati semanticamente (a meno di pattern noti)
- Niente adapter Figma diretto — la conversione Figma -> JSON neutro è step esterno
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PATTERNS_DIR = REPO_ROOT / "page-patterns"


class Report:
    def __init__(self):
        self.passes = []
        self.fails = []
        self.warns = []

    def ok(self, msg):
        self.passes.append(msg)

    def fail(self, msg):
        self.fails.append(msg)

    def warn(self, msg):
        self.warns.append(msg)

    def print(self):
        if self.passes:
            print("\n✅ Pass:")
            for m in self.passes:
                print(f"   {m}")
        if self.warns:
            print("\n⚠️  Warning:")
            for m in self.warns:
                print(f"   {m}")
        if self.fails:
            print("\n❌ Fail:")
            for m in self.fails:
                print(f"   {m}")
        print(f"\n--- Totale: {len(self.passes)} pass / {len(self.warns)} warn / {len(self.fails)} fail ---")

    def exit_code(self) -> int:
        return 1 if self.fails else 0


def load_pattern(page_type: str) -> dict:
    path = PATTERNS_DIR / page_type / "composition.json"
    if not path.is_file():
        print(f"❌ Pattern non trovato: {path}", file=sys.stderr)
        print(f"   Page-pattern disponibili:", file=sys.stderr)
        for d in sorted(PATTERNS_DIR.iterdir()):
            if d.is_dir() and (d / "composition.json").is_file():
                print(f"     - {d.name}", file=sys.stderr)
        sys.exit(2)
    with path.open() as f:
        return json.load(f)


def check_slots(pattern: dict, screen: dict, report: Report):
    slots = pattern.get("slots") or {}
    screen_slots = screen.get("slots") or {}

    for slot_name, slot_def in slots.items():
        present = bool(screen_slots.get(slot_name))
        if slot_def.get("required"):
            if present:
                report.ok(f"slot `{slot_name}` required → presente")
            else:
                report.fail(f"slot `{slot_name}` required ma ASSENTE")
            _check_slot_components(slot_name, slot_def, screen_slots.get(slot_name) or [], report)
        elif slot_def.get("forbidden"):
            if not present:
                report.ok(f"slot `{slot_name}` forbidden → assente")
            else:
                reason = slot_def.get("reason", "")
                report.fail(f"slot `{slot_name}` forbidden ma PRESENTE — {reason}")
        else:
            if present:
                _check_slot_components(slot_name, slot_def, screen_slots.get(slot_name) or [], report)

    unknown_slots = set(screen_slots) - set(slots)
    for s in sorted(unknown_slots):
        report.warn(f"slot `{s}` presente nella screen ma non definito nel pattern")


def _check_slot_components(slot_name: str, slot_def: dict, present_components: list, report: Report):
    allowed = slot_def.get("components")
    if not allowed:
        return
    allowed_lower = {c.lower() for c in allowed}
    for comp in present_components:
        if comp.lower() not in allowed_lower:
            report.fail(
                f"slot `{slot_name}`: componente `{comp}` non è nei componenti ammessi "
                f"({', '.join(allowed)})"
            )


def check_rules(pattern: dict, screen: dict, report: Report):
    rules = pattern.get("rules") or {}
    components = screen.get("componentsUsed") or []

    def slug_eq(c, slug):
        return (c.get("slug") or "").lower() == slug.lower()

    def has_prop(c, key, value):
        return (c.get("props") or {}).get(key, "").lower() == value.lower()

    if "maxPrimaryCTA" in rules:
        n = sum(1 for c in components if slug_eq(c, "button") and has_prop(c, "hierarchy", "primary"))
        limit = rules["maxPrimaryCTA"]
        msg = f"maxPrimaryCTA: {n}/{limit}"
        report.ok(msg) if n <= limit else report.fail(f"{msg} — troppi Button Primary")

    if "maxCardHighlight" in rules:
        n = sum(1 for c in components if slug_eq(c, "card-highlight"))
        limit = rules["maxCardHighlight"]
        msg = f"maxCardHighlight: {n}/{limit}"
        report.ok(msg) if n <= limit else report.fail(f"{msg} — troppe Card Highlight")

    if "maxCardEntrypoint" in rules:
        n = sum(1 for c in components if slug_eq(c, "card-entrypoint"))
        limit = rules["maxCardEntrypoint"]
        msg = f"maxCardEntrypoint: {n}/{limit}"
        report.ok(msg) if n <= limit else report.fail(f"{msg} — troppe Card Entrypoint")

    custom = rules.get("customRules") or []
    for r in custom:
        report.warn(f"custom rule (verifica manuale): {r}")


def list_anti_patterns(pattern: dict, report: Report):
    aps = pattern.get("antiPatterns") or []
    for ap in aps:
        report.warn(
            f"antiPattern `{ap.get('scenario', '?')}` da verificare manualmente — "
            f"{ap.get('reason', '')[:120]}…"
        )


def main():
    parser = argparse.ArgumentParser(description="Confronta una schermata contro il page-pattern")
    parser.add_argument("--screen", required=True, help="Path al JSON della schermata")
    parser.add_argument("--page-type", help="Override del pageType (altrimenti letto dallo screen JSON)")
    args = parser.parse_args()

    screen_path = Path(args.screen)
    if not screen_path.is_file():
        print(f"❌ File non trovato: {screen_path}", file=sys.stderr)
        sys.exit(2)

    with screen_path.open() as f:
        screen = json.load(f)

    page_type = args.page_type or screen.get("pageType")
    if not page_type:
        print("❌ pageType non specificato (né in screen JSON né con --page-type)", file=sys.stderr)
        sys.exit(2)

    pattern = load_pattern(page_type)

    print(f"🔍 Scoring schermata `{screen_path.name}` contro pattern `{page_type}`")
    print(f"   Status pattern: {pattern.get('status', '?')}")
    if pattern.get("status") != "full":
        print(f"   ⚠️  Pattern in status `{pattern.get('status')}` — il risultato è indicativo "
              f"finché l'UX team non promuove a `full`.")

    report = Report()
    check_slots(pattern, screen, report)
    check_rules(pattern, screen, report)
    list_anti_patterns(pattern, report)
    report.print()
    sys.exit(report.exit_code())


if __name__ == "__main__":
    main()
