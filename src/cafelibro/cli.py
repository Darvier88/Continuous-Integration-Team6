from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import (
    CafeLibroError,
    load_state,
    save_state,
    register_book,
    register_member,
    loan_book,
    return_book,
    list_member_loans,
    overdue_loans,
)

DEFAULT_DB = Path("data/library.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cafelibro", description="CaféLibro library loan manager")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to JSON storage file")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add-book", help="Register a book in the catalogue")
    p.add_argument("code")
    p.add_argument("title")

    p = sub.add_parser("add-member", help="Register a library member")
    p.add_argument("member_id")
    p.add_argument("name")

    p = sub.add_parser("loan", help="Loan a book to a member")
    p.add_argument("book_code")
    p.add_argument("member_id")
    p.add_argument("due_date")

    p = sub.add_parser("return", help="Return a book")
    p.add_argument("book_code")

    p = sub.add_parser("member-loans", help="List books a member currently has")
    p.add_argument("member_id")

    p = sub.add_parser("overdue", help="Report overdue loans")
    p.add_argument("--today", help="Override current date using YYYY-MM-DD")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    state = load_state(args.db)

    try:
        changed = True
        if args.command == "add-book":
            result = register_book(state, args.code, args.title)
        elif args.command == "add-member":
            result = register_member(state, args.member_id, args.name)
        elif args.command == "loan":
            result = loan_book(state, args.book_code, args.member_id, args.due_date)
        elif args.command == "return":
            result = return_book(state, args.book_code)
        elif args.command == "member-loans":
            changed = False
            result = list_member_loans(state, args.member_id)
        elif args.command == "overdue":
            changed = False
            result = overdue_loans(state, args.today)
        else:
            raise CafeLibroError("Unknown command")

        if changed:
            save_state(args.db, state)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except CafeLibroError as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
