"""Automated checks for Activity 7: Fruit Stand.

Every check reads the stand log at the end of the run, never the lines
printed along the way, so the wording is yours. Log values are matched
loosely: any amount of whitespace, any letter case, and the colon is
optional, so `print("Pieces:", pieces)`, `print("Pieces: " + str(pieces))`
and `print(f"Pieces: {pieces}")` all read the same.

Most checks replace the provided dictionaries with different ones before
running, so a number that was counted by eye and typed in passes only for the
stock it was counted from. Take every number from the dictionaries.

When a check fails, the assertion message says which log line came out wrong,
what it said, what was expected, and the stock that was used.
"""

import re
from unittest.mock import patch

import main
from main import main as run_main

# The order the starter asks its questions.
QUESTIONS = ["name", "sell_fruit", "sell_amount", "restock_fruit", "restock_amount", "restock_price"]

SAFE = dict(
    name="JJ",
    sell_fruit="apples",
    sell_amount=1,
    restock_fruit="pears",
    restock_amount=1,
    restock_price=4,
)

OTHER_STOCK = {"kiwis": 6, "limes": 0, "figs": 9}
OTHER_PRICES = {"kiwis": 2, "limes": 1, "figs": 10}


def run(capsys, stock=None, prices=None, **changes):
    """Run main() once, optionally against different dictionaries."""
    answers = {**SAFE, **changes}
    if stock is not None:
        answers = {**SAFE, "sell_fruit": "kiwis", "restock_fruit": "figs", **changes}
    typed = [str(answers[q]) for q in QUESTIONS]
    original = main.stock, main.prices
    if stock is not None:
        main.stock, main.prices = dict(stock), dict(prices)
    else:
        main.stock, main.prices = dict(main.stock), dict(main.prices)
    used = dict(main.stock), dict(main.prices)
    try:
        with patch("builtins.input", side_effect=typed):
            run_main()
    finally:
        main.stock, main.prices = original
    out, err = capsys.readouterr()
    assert err == "", "the program wrote to the error stream:\n" + err
    return out, answers, used


def log_value(out, label):
    """Return the value printed after `label` in the stand log, normalized."""
    start = out.upper().find("STAND LOG")
    if start < 0:
        return None
    words = r"\s+".join(re.escape(word) for word in label.split())
    match = re.search(rf"^[ \t]*{words}[ \t]*:?[ \t]*([^\n]*)", out[start:], re.IGNORECASE | re.MULTILINE)
    if match is None:
        return None
    return " ".join(match.group(1).split()).upper().rstrip(".! ")


def expect(capsys, label, want, stock=None, prices=None, **changes):
    """Run once and check that the stand log line `label` says `want`."""
    out, answers, used = run(capsys, stock=stock, prices=prices, **changes)
    context = (
        f"stock: {used[0]}, prices: {used[1]}, sold {answers['sell_amount']} "
        f"{answers['sell_fruit']}, restocked {answers['restock_amount']} {answers['restock_fruit']}"
    )
    if "STAND LOG" not in out.upper():
        raise AssertionError(f"no \"STAND LOG\" line was printed ({context})")
    got = log_value(out, label)
    if got is None:
        raise AssertionError(f'no "{label}" line was printed after STAND LOG ({context})')
    # A printed list may or may not have spaces after its commas, and may use either quote.
    squash = lambda text: text.replace(" ", "").replace('"', "'")
    assert squash(got) == squash(str(want).upper()), (
        f'the "{label}" line said {got}, expected {want} ({context})'
    )


def test_counts_kinds_pieces_and_value(capsys):
    expect(capsys, "STAND LOG", "JJ")
    expect(capsys, "Kinds before", 4)
    expect(capsys, "Pieces", 25)
    # 12 * 3 + 5 * 4 + 0 * 5 + 8 * 7 is 112
    expect(capsys, "Stock value", 112)
    # Different dictionaries, so numbers typed in by hand do not pass.
    expect(capsys, "Kinds before", 3, stock=OTHER_STOCK, prices=OTHER_PRICES)
    expect(capsys, "Pieces", 15, stock=OTHER_STOCK, prices=OTHER_PRICES)
    expect(capsys, "Stock value", 102, stock=OTHER_STOCK, prices=OTHER_PRICES)


def test_out_of_stock_lists_the_fruits_with_none_left(capsys):
    expect(capsys, "Out of stock", "['plums']")
    expect(capsys, "Out of stock", "['limes']", stock=OTHER_STOCK, prices=OTHER_PRICES)
    # Nothing is sold out, so the list is empty.
    expect(capsys, "Out of stock", "[]", stock={"kiwis": 6}, prices={"kiwis": 2})


def test_a_sale_with_enough_stock(capsys):
    expect(capsys, "Sale", "SOLD", sell_fruit="apples", sell_amount=5)
    expect(capsys, "Sold", 5, sell_fruit="apples", sell_amount=5)
    expect(capsys, "Revenue", 15, sell_fruit="apples", sell_amount=5)
    expect(capsys, "Left", 7, sell_fruit="apples", sell_amount=5)
    # Selling exactly what is left is still a full sale.
    expect(capsys, "Sale", "SOLD", sell_fruit="pears", sell_amount=5)
    expect(capsys, "Left", 0, sell_fruit="pears", sell_amount=5)
    expect(capsys, "Revenue", 10, stock=OTHER_STOCK, prices=OTHER_PRICES, sell_fruit="figs", sell_amount=1)


def test_a_sale_for_more_than_is_left(capsys):
    # 20 apples were asked for and 12 are there: sell the 12.
    expect(capsys, "Sale", "SHORT", sell_fruit="apples", sell_amount=20)
    expect(capsys, "Sold", 12, sell_fruit="apples", sell_amount=20)
    expect(capsys, "Revenue", 36, sell_fruit="apples", sell_amount=20)
    expect(capsys, "Left", 0, sell_fruit="apples", sell_amount=20)
    # A fruit with none at all sells nothing.
    expect(capsys, "Sale", "SHORT", sell_fruit="plums", sell_amount=2)
    expect(capsys, "Sold", 0, sell_fruit="plums", sell_amount=2)


def test_a_sale_of_a_fruit_the_stand_does_not_carry(capsys):
    expect(capsys, "Sale", "UNKNOWN", sell_fruit="mangoes", sell_amount=3)
    expect(capsys, "Sold", 0, sell_fruit="mangoes", sell_amount=3)
    expect(capsys, "Revenue", 0, sell_fruit="mangoes", sell_amount=3)
    # Asking for a missing fruit must not add it to the stock.
    expect(capsys, "Kinds after", 4, sell_fruit="mangoes", sell_amount=3, restock_fruit="pears")


def test_restocking_a_fruit_already_carried(capsys):
    # 5 pears plus 10 more, at a new price.
    expect(capsys, "Restocked", 15, restock_fruit="pears", restock_amount=10, restock_price=6)
    expect(capsys, "Price", 6, restock_fruit="pears", restock_amount=10, restock_price=6)
    expect(capsys, "Kinds after", 4, restock_fruit="pears", restock_amount=10, restock_price=6)
    # The sale happens first, so selling apples and restocking them adds to what is left.
    expect(capsys, "Restocked", 17, sell_fruit="apples", sell_amount=5, restock_fruit="apples", restock_amount=10)


def test_restocking_a_new_fruit(capsys):
    expect(capsys, "Restocked", 9, restock_fruit="figs", restock_amount=9, restock_price=8)
    expect(capsys, "Price", 8, restock_fruit="figs", restock_amount=9, restock_price=8)
    expect(capsys, "Kinds after", 5, restock_fruit="figs", restock_amount=9, restock_price=8)
    expect(
        capsys, "Kinds after", 4, stock=OTHER_STOCK, prices=OTHER_PRICES,
        restock_fruit="dates", restock_amount=2, restock_price=5,
    )
