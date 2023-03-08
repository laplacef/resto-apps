from datetime import date as dt


def welcome_user() -> None:
    """Prints welcome message to user."""

    print("Welcome! Please select the choices you want. Press 'r' when you're ready.")


def print_menu() -> None:
    """Print menu to user screen."""

    print(
        f"Menu:\n1. Sandwich ($10) - 10% discount if you order 5 or more\n2. Salad ($8) - 10% discount if ordered with a soup.\n3. Soup ($6) - 20% if ordered with a sandwich and salad.\n4. Coffee/Tea ($5)"
    )


def get_user_name() -> str:
    """Gets and stores user name."""

    user_name = input(f"Please enter your name: ")

    return user_name.capitalize()


def get_user_choices() -> list:
    """Gets and stores user food choices."""

    user_choices = []
    while True:
        user_input = input(
            "Enter your number choices from the menu, press 'r' when you're ready: "
        )
        if user_input.lower() == "r":
            break
        else:
            try:
                user_input = int(user_input)
            except ValueError:
                print(
                    f"Enter a numerical choice from the menu. Enter 'r' when you're ready."
                )
            else:
                if user_input not in [1, 2, 3, 4]:
                    print("Please enter a choice from the menu (1-4)")
                else:
                    user_choices.append(user_input)

    return user_choices


def calculate_prep_time(user_choices: list, item_list: list) -> int:
    """Returns estimated prep time based on items ordered."""

    prep_time_mins = 0
    for item in user_choices:
        prep_time_mins += item_list[item][4]
    hours = prep_time_mins // 60
    minutes = prep_time_mins % 60
    prep_time = f"{hours}h: {minutes}m"

    return prep_time


def calculate_prices(user_choices: list, item_list: list) -> dict:
    """Return prices for each item on sale."""

    prices = {}
    for item in set(user_choices):
        prices.update({item: item_list[item][2] * user_choices.count(item)})

    return prices


def calculate_discount(user_choices: list, prices: dict, item_list: list) -> float:
    """Return any discounts or specials applied to associated items."""

    discounted_prices = prices.copy()
    for item, value in discounted_prices.items():
        if (item == 1) and (user_choices.count(1) >= 5):
            discounted_prices[item] = round(value - (value * item_list[item][3]), 2)
        elif (item == 2) and (3 in discounted_prices.keys()):
            discounted_prices[item] = round(value - (value * item_list[item][3]), 2)
        elif (item == 3) and ((1 and 2) in discounted_prices.keys()):
            discounted_prices[item] = round(value - (value * item_list[item][3]), 2)
        else:
            discounted_prices[item] = round(value, 2)

    return discounted_prices


def calculate_tax(discounted_prices: dict) -> float:
    """Return tax aomunt (based on CA tax)."""

    ca_tax = 0.0725

    tax = ca_tax * sum(discounted_prices.values())

    return tax


def calculate_total(discounted_prices, tax) -> float:
    """Returns the total price plus tax."""

    total = sum(discounted_prices.values()) + tax

    return total


def print_receipt(
    user_name: str,
    user_choices: list,
    prep_time,
    discounted_prices: dict,
    tax: float,
    total: float,
    item_list: list,
) -> None:
    """Print final receipt with subtotal, total. tax, and additional customer info."""

    print(f"*" * 50)
    print(f"{user_name}, thanks for your order!\n",)
    print(f"Items\t\tQuantity\tPrice")
    for item, value in discounted_prices.items():
        if item == 1:
            print(
                f"{item_list[item][1]}\t   {user_choices.count(item)}\t\t{format(value, '.2f')}"
            )
        else:
            print(
                f"{item_list[item][1]}\t\t   {user_choices.count(item)}\t\t{format(value, '.2f')}"
            )
    print(f"\nSubtotal\t${format(sum(discounted_prices.values()), '.2f')}")
    print(f"Tax\t\t${format(tax, '.2f')}")
    print(f"Total\t\t${format(total, '.2f')}")
    print(f"\n{dt.today()}, Your order will be ready in {prep_time}")
    print(f"*" * 50)


def main() -> None:
    """Run receipts app."""

    item_list = [
        ["Id", "Item", "Price ($)", "Discount (%)", "Preparation Time (Mins.)"],
        [1, "Sandwich", 10, 0.10, 10],
        [2, "Salad", 8, 0.10, 8],
        [3, "Soup", 6, 0.20, 15],
        [4, "Coffee/Tea", 5, 0, 5],
    ]

    welcome_user()
    print_menu()
    user_name = get_user_name()
    user_choices = get_user_choices()
    prep_time = calculate_prep_time(user_choices, item_list)
    prices = calculate_prices(user_choices, item_list)
    discounted_prices = calculate_discount(user_choices, prices, item_list)
    tax = calculate_tax(discounted_prices)
    total = calculate_total(discounted_prices, tax)
    print_receipt(
        user_name, user_choices, prep_time, discounted_prices, tax, total, item_list
    )


if __name__ == "__main__":
    main()
