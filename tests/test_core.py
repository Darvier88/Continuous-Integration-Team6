import pytest

from cafelibro.core import (
    CafeLibroError,
    register_book,
    register_member,
    loan_book,
    return_book,
    list_member_loans,
    overdue_loans,
)


def empty_state():
    return {"books": [], "members": [], "loans": []}


def seed_state():
    state = empty_state()
    register_book(state, "B001", "Clean Code")
    register_member(state, "M001", "Ana Torres")
    return state


def test_register_book_with_unique_code():
    state = empty_state()
    book = register_book(state, "B001", "Clean Code")
    assert book == {"code": "B001", "title": "Clean Code"}
    assert state["books"] == [book]


def test_register_book_rejects_duplicate_code():
    state = empty_state()
    register_book(state, "B001", "Clean Code")
    with pytest.raises(CafeLibroError, match="already exists"):
        register_book(state, "B001", "Other Title")


def test_register_member_with_unique_identifier():
    state = empty_state()
    member = register_member(state, "M001", "Ana Torres")
    assert member == {"member_id": "M001", "name": "Ana Torres"}


def test_register_member_rejects_duplicate_identifier():
    state = empty_state()
    register_member(state, "M001", "Ana Torres")
    with pytest.raises(CafeLibroError, match="already exists"):
        register_member(state, "M001", "Luis Cedeño")


def test_loan_book_to_member():
    state = seed_state()
    loan = loan_book(state, "B001", "M001", "2026-06-20")
    assert loan == {"book_code": "B001", "member_id": "M001", "due_date": "2026-06-20"}


def test_loan_rejects_book_already_on_loan():
    state = seed_state()
    loan_book(state, "B001", "M001", "2026-06-20")
    with pytest.raises(CafeLibroError, match="already on loan"):
        loan_book(state, "B001", "M001", "2026-06-21")


def test_member_cannot_hold_more_than_three_books():
    state = empty_state()
    register_member(state, "M001", "Ana Torres")
    for code in ["B001", "B002", "B003", "B004"]:
        register_book(state, code, f"Book {code}")
    loan_book(state, "B001", "M001", "2026-06-20")
    loan_book(state, "B002", "M001", "2026-06-20")
    loan_book(state, "B003", "M001", "2026-06-20")
    with pytest.raises(CafeLibroError, match="more than 3"):
        loan_book(state, "B004", "M001", "2026-06-20")


def test_return_book_marks_it_available_again():
    state = seed_state()
    loan_book(state, "B001", "M001", "2026-06-20")
    returned = return_book(state, "B001")
    assert returned["book_code"] == "B001"
    assert state["loans"] == []
    loan_book(state, "B001", "M001", "2026-07-01")
    assert len(state["loans"]) == 1


def test_list_books_member_currently_has_on_loan():
    state = seed_state()
    register_book(state, "B002", "Refactoring")
    loan_book(state, "B001", "M001", "2026-06-20")
    loan_book(state, "B002", "M001", "2026-06-21")
    loans = list_member_loans(state, "M001")
    assert [loan["title"] for loan in loans] == ["Clean Code", "Refactoring"]


def test_report_overdue_loans():
    state = seed_state()
    loan_book(state, "B001", "M001", "2026-06-01")
    assert overdue_loans(state, today="2026-06-10")[0]["book_code"] == "B001"
    assert overdue_loans(state, today="2026-05-31") == []
