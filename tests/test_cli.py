import json

from cafelibro.cli import main


def test_cli_add_book_persists_to_json_file(tmp_path, capsys):
    db = tmp_path / "library.json"
    exit_code = main(["--db", str(db), "add-book", "B001", "Clean Code"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out)["code"] == "B001"
    data = json.loads(db.read_text(encoding="utf-8"))
    assert data["books"][0]["title"] == "Clean Code"


def test_cli_returns_error_code_for_invalid_operation(tmp_path, capsys):
    db = tmp_path / "library.json"
    exit_code = main(["--db", str(db), "return", "B999"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error:" in captured.out
