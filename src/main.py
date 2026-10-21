"""Fruit Stand.

CMPSC 100: Computational Expression, Activity 7

A fruit stand at the farmers market keeps its stock and its prices in two
dictionaries. Count the stock, sell some of one fruit, and restock.

The dictionaries below are provided. Your program should work for any stock
and any prices, so take every number it reports from the dictionaries
themselves rather than counting by eye.

Author: TODO
"""

stock = {"apples": 12, "pears": 5, "plums": 0, "cherries": 8}
prices = {"apples": 3, "pears": 4, "plums": 5, "cherries": 7}


def main():
    print("=" * 50)
    print("FRUIT STAND")
    print("=" * 50)

    # TODO 1: ask six questions, in this order, and save each answer to the
    # variable named here. Convert the numbers with int
    # `name`: the user's name
    # `sell_fruit`: which fruit the customer wants
    # `sell_amount`: how many (an int)
    # `restock_fruit`: which fruit arrived from the farm
    # `restock_amount`: how many arrived (an int)
    # `restock_price`: its price (an int)

    # TODO 2: set `pieces` to 0, `value` to 0, `sold_out` to an empty list,
    # and `kinds` to the number of entries in `stock`

    # TODO 3: write one for loop over `stock`. On every trip/iteration, with
    # `fruit` holding the key:
    # add that fruit's quantity to `pieces`
    # add its quantity times its price to `value`
    # if its quantity is 0, append the fruit to `sold_out`

    # TODO 4: the sale. Check whether `sell_fruit` is a key of `stock` before
    # looking it up
    # if it is not a key: save "UNKNOWN" to `sale` and 0 to `sold`
    # otherwise, if `sell_amount` is more than the quantity in stock: save
    # "SHORT" to `sale` and the whole quantity in stock to `sold`
    # otherwise: save "SOLD" to `sale` and `sell_amount` to `sold`
    # Then set `revenue` and `left` to 0. If `sell_fruit` is a key, subtract
    # `sold` from its quantity, save `sold` times its price to `revenue`, and
    # save the quantity now in stock to `left`

    # TODO 5: the restock. If `restock_fruit` is a key of `stock`, add
    # `restock_amount` to its quantity. Otherwise add it to `stock` with
    # `restock_amount` as its quantity. Either way, set its price in `prices`
    # to `restock_price`

    # TODO 6: print a blank line, a line of 50 "=", "STAND LOG:" followed by
    # the name, and another line of 50 "=". Then print these lines, each a
    # label followed by its value:
    # Kinds before: `kinds`
    # Pieces: `pieces`
    # Stock value: `value`
    # Out of stock: `sold_out`
    # Sale: `sale`
    # Sold: `sold`
    # Revenue: `revenue`
    # Left: `left`
    # Kinds after: the number of entries in `stock` now
    # Restocked: the quantity of `restock_fruit` now in stock
    # Price: the price of `restock_fruit` now in `prices`


if __name__ == "__main__":
    main()
