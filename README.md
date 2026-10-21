# Activity 7: Fruit Stand

|Item |       |
|:----|:------|
|Released |Wednesday, October 28, in class |
|Due |Monday, November 2, 9:00am |
|Progress |[![Grade](../../actions/workflows/main.yml/badge.svg?branch=main)](../../actions/workflows/main.yml) |

A fruit stand at the farmers market keeps its stock and its prices in two dictionaries. Your
program counts the stock, sells some of one fruit, and restocks. If a step confuses you, please
ask about it while you are still in the room.

## Course learning outcomes

This activity addresses the following course learning outcomes:

**CLO 1.** Apply Python programming fundamentals to execute and explain computer code that
implements interactive, novel solutions to a variety of computable problems.

**CLO 2.** Implement code consistent with industry-standard practices using professional-grade
integrated development environments (IDEs), command-line tools, and version control systems.

Specifically, by the end of this activity you should be able to:

* read a value from a dictionary by its key
* test whether a key is in a dictionary with `in` and `not in`
* add an entry and change an entry by assigning to a key
* count the entries of a dictionary with `len`
* visit every key of a dictionary with `for fruit in stock`
* look up a second dictionary with the same key

## The problem

The two dictionaries are provided at the top of `src/main.py`:

```python
stock = {"apples": 12, "pears": 5, "plums": 0, "cherries": 8}
prices = {"apples": 3, "pears": 4, "plums": 5, "cherries": 7}
```

`stock` maps each fruit to the quantity on hand, and `prices` maps each fruit to its price in
dollars.

**Your program has to work for any stock and any prices, not just these.** Take every number it
reports from the dictionaries themselves. A number counted by eye and typed in is right until
the dictionaries change, and the automated checks run your program against different ones.

Your program asks six questions, counts the stock, makes one sale, makes one restock, and ends
with a stand log:

|Value |Where it comes from |
|:-----|:-------------------|
|`Kinds before` |How many fruits `stock` holds before the sale |
|`Pieces` |The total of every quantity before the sale |
|`Stock value` |Quantity times price, added up for every fruit before the sale |
|`Out of stock` |A list of the fruits whose quantity is `0` before the sale |
|`Sale` |`SOLD` when the stock covers the amount asked for, `SHORT` when it does not, `UNKNOWN` when the fruit is not in `stock` |
|`Sold` |The amount sold: what was asked for, or all that was left when `SHORT`, or `0` when `UNKNOWN` |
|`Revenue` |`Sold` times that fruit's price, or `0` when `UNKNOWN` |
|`Left` |The quantity of that fruit after the sale, or `0` when `UNKNOWN` |
|`Kinds after` |How many fruits `stock` holds after the restock |
|`Restocked` |The quantity of the restocked fruit after the restock |
|`Price` |The price of the restocked fruit after the restock |

The sale happens before the restock. A fruit that is not in `stock` has no quantity and no
price, so the program checks with `in` before it looks anything up, and a sale of an unknown
fruit adds nothing to either dictionary. A restocked fruit that is already in `stock` gains the
amount that arrived. A restocked fruit that is not in `stock` becomes a new entry with that
amount. Either way, its price in `prices` becomes the price given.

### Example run

```text
$ uv run python src/main.py
==================================================
FRUIT STAND
==================================================
What is your name? JJ
Which fruit does the customer want? apples
How many? 5
Which fruit arrived from the farm? plums
How many arrived? 10
What is its price? 6

==================================================
STAND LOG: JJ
==================================================
Kinds before: 4
Pieces: 25
Stock value: 112
Out of stock: ['plums']
Sale: SOLD
Sold: 5
Revenue: 15
Left: 7
Kinds after: 4
Restocked: 10
Price: 6
```

Your wording is yours. The checks read only the stand log at the end, they forgive extra
spaces and letter case, and any of the three ways to print a value passes:
`print("Pieces:", pieces)`, `print("Pieces: " + str(pieces))`, or `print(f"Pieces: {pieces}")`.

Ask the six questions in this order: name, fruit to sell, how many, fruit that arrived, how
many arrived, its price.

## Getting started

Open `src/main.py` and work through the `TODO` markers in order. Run it as you go, rather than
writing all of it and running it once:

```text
uv run python src/main.py
```

Put your name on the `Author:` line at the top of the file, and delete each `TODO` marker as
you finish that step.

## Evaluation

In-class activities are graded on completion and contribute to the **In-Class Activities**
category on the syllabus (10 points, averaged across the semester). This activity is worth one
activity grade. What is graded is the attempt, not whether every value comes out right.

|Level |What it looks like |
|:-----|:------------------|
|**Complete** |At least half of the activity is done |
|**Partial** |Less than half is done, but something beyond the starter was committed |
|**Incomplete** |Nothing was changed |

Run the automated checks yourself, as many times as you like, from the top folder of this
repository rather than from inside `src`:

```text
uv run gatorgrade --config gatorgrade.yml
```

Each check's description says what to look at when it fails. Under a failed check, gatorgrade
also prints a `uv run pytest ...` command. Run it: the last lines name the log line that came
out wrong, what it said, what was expected, and the stock that was used.

> [!NOTE]
> Automated results are preliminary. Your instructor sets the final grade.

## Submitting

Commit and push often. The last version pushed before the deadline is the one that gets
graded.

**In the terminal:**

```text
git add src/main.py
git commit -m "Complete the fruit stand activity"
git push
```

**In VS Code**, the Source Control panel in the left sidebar does the same three steps:

1. Click **+** next to a changed file to stage it, which is `git add`
2. Type a message in the box at the top, then click the checkmark, which is `git commit`
3. Click **Sync Changes** (or the up arrow) to push

Either way, then open your repository on GitHub and confirm your latest changes are actually
there.

If you need more time, apply a late token with [this form](https://forms.gle/3nGbpaNrG96DpLLdA).
