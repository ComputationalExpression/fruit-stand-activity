"""Structure checks for Activity 7: Fruit Stand.

These read `src/main.py` as Python, not as text, so the words in the TODO
comments do not count. Only real statements do.
"""

import ast
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "src" / "main.py"


def tree():
    return ast.parse(SOURCE.read_text(encoding="utf-8"))


def nodes(kind):
    return [n for n in ast.walk(tree()) if isinstance(n, kind)]


def test_a_for_loop_over_the_stock_and_an_in_check():
    found = [
        loop for loop in nodes(ast.For)
        if isinstance(loop.iter, ast.Name) and loop.iter.id == "stock"
    ]
    assert found, "found no `for ... in stock:` loop: one pass over the keys does the counting"
    checks = [
        n for n in nodes(ast.Compare)
        if any(isinstance(op, (ast.In, ast.NotIn)) for op in n.ops)
    ]
    assert checks, "found no `in` or `not in` check: test whether a fruit is a key before looking it up"


def test_entries_are_changed_and_added_by_assigning_to_a_key():
    stores = [
        n for n in nodes(ast.Subscript)
        if isinstance(n.ctx, ast.Store) and isinstance(n.value, ast.Name)
    ]
    targets = {n.value.id for n in stores}
    assert "stock" in targets, "found no `stock[...] = ...`: a sale and a restock both change an entry"
    assert "prices" in targets, "found no `prices[...] = ...`: the restock sets the fruit's price"
