from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

MAX_LOANS_PER_MEMBER = 3


class CafeLibroError(ValueError):
    """Domain error with a clear message for CLI users."""


@dataclass
class Book:
    code: str
    title: str


@dataclass
class Member:
    member_id: str
    name: str


@dataclass
class Loan:
    book_code: str
    member_id: str
    due_date: str  # ISO format YYYY-MM-DD


EMPTY_STATE: dict[str, Any] = {"books": [], "members": [], "loans": []}


def load_state(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        save_state(file_path, EMPTY_STATE.copy())
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for key in EMPTY_STATE:
        data.setdefault(key, [])
    return data


def save_state(path: str | Path, state: dict[str, Any]) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _find(items: list[dict[str, Any]], key: str, value: str) -> dict[str, Any] | None:
    return next((item for item in items if item.get(key) == value), None)


def register_book(state: dict[str, Any], code: str, title: str) -> dict[str, Any]:
    if _find(state["books"], "code", code):
        raise CafeLibroError(f"Book code already exists: {code}")
    book = Book(code=code, title=title)
    state["books"].append(asdict(book))
    return asdict(book)


def register_member(state: dict[str, Any], member_id: str, name: str) -> dict[str, Any]:
    if _find(state["members"], "member_id", member_id):
        raise CafeLibroError(f"Member identifier already exists: {member_id}")
    member = Member(member_id=member_id, name=name)
    state["members"].append(asdict(member))
    return asdict(member)


def loan_book(state: dict[str, Any], book_code: str, member_id: str, due_date: str) -> dict[str, Any]:
    if not _find(state["books"], "code", book_code):
        raise CafeLibroError(f"Book does not exist: {book_code}")
    if not _find(state["members"], "member_id", member_id):
        raise CafeLibroError(f"Member does not exist: {member_id}")
    if _find(state["loans"], "book_code", book_code):
        raise CafeLibroError(f"Book is already on loan: {book_code}")
    member_loans = [loan for loan in state["loans"] if loan["member_id"] == member_id]
    if len(member_loans) >= MAX_LOANS_PER_MEMBER:
        raise CafeLibroError(f"Member cannot hold more than {MAX_LOANS_PER_MEMBER} books")
    _parse_date(due_date)
    loan = Loan(book_code=book_code, member_id=member_id, due_date=due_date)
    state["loans"].append(asdict(loan))
    return asdict(loan)


def return_book(state: dict[str, Any], book_code: str) -> dict[str, Any]:
    loan = _find(state["loans"], "book_code", book_code)
    if loan is None:
        raise CafeLibroError(f"Book is not currently on loan: {book_code}")
    state["loans"].remove(loan)
    return loan


def list_member_loans(state: dict[str, Any], member_id: str) -> list[dict[str, Any]]:
    if not _find(state["members"], "member_id", member_id):
        raise CafeLibroError(f"Member does not exist: {member_id}")
    books_by_code = {book["code"]: book for book in state["books"]}
    result = []
    for loan in state["loans"]:
        if loan["member_id"] == member_id:
            book = books_by_code.get(loan["book_code"], {})
            result.append({**loan, "title": book.get("title", "Unknown")})
    return result


def overdue_loans(state: dict[str, Any], today: str | None = None) -> list[dict[str, Any]]:
    current_date = _parse_date(today) if today else date.today()
    books_by_code = {book["code"]: book for book in state["books"]}
    members_by_id = {member["member_id"]: member for member in state["members"]}
    overdue = []
    for loan in state["loans"]:
        if _parse_date(loan["due_date"]) < current_date:
            overdue.append({
                **loan,
                "title": books_by_code.get(loan["book_code"], {}).get("title", "Unknown"),
                "member_name": members_by_id.get(loan["member_id"], {}).get("name", "Unknown"),
            })
    return overdue


def _parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise CafeLibroError("Date must use YYYY-MM-DD format") from exc
