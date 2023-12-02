from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich import box
import time
import random
import sys


class Coffee:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @name.setter
    def name(self, name):
        self._name = name

    @price.setter
    def price(self, price):
        self._price = price

class Receipt:
    def __init__(self, total=0, name="", order_number=0):
        self.total = total
        self.name = name
        self.order_number = order_number

    @property
    def total(self):
        return self._total

    @property
    def name(self):
        return self._name

    @property
    def order_number(self):
        return self._order_number

    @total.setter
    def total(self, total):
        self._total = total

    @name.setter
    def name(self, name):
        self._name = name

    @order_number.setter
    def order_number(self, order_number):
        self._order_number = order_number

espresso = Coffee("Espresso", 1.69)
latte = Coffee("Latte", 2.59)
americano = Coffee("Americano", 1.59)
cappuccino = Coffee("Cappuccino", 2.69)
mocha = Coffee("Mocha", 4.99)
macchiato = Coffee("Macchiato", 3.29)
iced = Coffee("Iced", 4.99)
black = Coffee("Black", 1.99)
frappe = Coffee("Frappe", 3.99)
irish = Coffee("Irish", 2.59)

price = 0


def main():

    console = Console()

    coffees = [espresso, latte, americano, cappuccino, mocha,macchiato,iced,black,frappe,irish]

    selection = {f"{espresso.name}":0, f"{latte.name}":0, f"{americano.name}":0, f"{cappuccino.name}":0, f"{mocha.name}":0,
                 f"{macchiato.name}":0,f"{iced.name}":0,f"{black.name}":0,f"{frappe.name}":0,f"{irish.name}":0}

    while True:
        print_offer(coffees,selection)
        n = input("Enter: ")

        if n == 'F' or n == 'f':
            break

        if n == 'e' or n =='E':
            console.print("Bye bye 👋")
            sys.exit()

        try:
            n = int(n)
            if n < 0 or n > 10:
                console.print("Invalid key ☹️", style="bold red")
        except:
            console.print("Invalid key ☹️", style="bold red")
            continue

        if n > 0 and n < 11:
            add_to_order(n-1,coffees)
            selection[coffees[n-1].name] += 1

        if n == 0:
            removed_item = remove_from_order(selection)
            if removed_item == -1:
                console.print("Your order is empty!", style ="bold red")
            elif removed_item == False:
                continue
            else:
                console.print("Success!", style="green",)
                console.print("REMOVED: ", style="red", end="")
                console.print(removed_item)
                selection[removed_item] -= 1

    # Print total
    if price < 1:
        console.print("Your order is empty 😕", style="italic")
        sys.exit()
    console.print("Your total is: ",end="",style="italic")
    console.print(f"$ {round(price,2)}", style="bold #98FB98")

    # Prompt user for their credit card number
    while True:
        try:
            console.print("Please enter your credit card number: ", style="italic", end="")
            credit_card = int(input())

            if validator(credit_card) == False:
                for i in track(range(20), description="Processing..."):
                    time.sleep(0.1)
                console.print("INVALID credit card!",style="bold red")
                continue
            else:
                for i in track(range(20), description="Processing..."):
                    time.sleep(0.1)
                console.print(f"APPROVED! ",style="bold green", end="")
                console.print(f"{validator(credit_card)}",style="italic cyan")
                break

        except ValueError:
            console.print("Invalid usage!", style="bold red")

    # Prompt user for their name
    while True:
        console.print("Enter your first name: ", style="italic", end="")
        name = str(input(""))
        if name.isalpha() != True:
            console.print("Invalid usage!", style="bold red")
        else:
            break

    # Generate order id
    order_number = random.randint(2,10000)

    receipt = Receipt(price, name, order_number)

    total = print_receipt(selection, receipt)


def print_offer(coffees, selection):
    console = Console()
    tab = Table(title="☕ Coffee shop ☕", box = box.ROUNDED, caption="type index to add to order\n[0] to remove from order\n[F] to pay\n[E] to exit")

    S = all(value == 0 for value in selection.values())

    tab.add_column("Index", style="bold	#87CEEB", justify="center")
    tab.add_column("Name", style="bold italic #9966cc", justify="center")
    tab.add_column("Price", style="#98FB98", justify="right")
    if S == False:
        tab.add_column("", style="#98FB98", justify="right")

        tab.add_column("Current selection", style="bold italic #9966cc", justify="right")
        tab.add_column("Quantity", style="bold	#87CEEB", justify="center")


        select = {key: value for key, value in selection.items() if value > 0}
        names = list(select.keys())

    for i in range(len(coffees)):
        try:
            tab.add_row(str(i+1),coffees[i].name,f"${coffees[i].price}","☕",f"{names[i]}",f"{select[names[i]]}")
        except:
            tab.add_row(str(i+1),coffees[i].name,f"${coffees[i].price}","☕")

    console.print(tab)


def add_to_order(n, coffees):
    if not n or not coffees or n < 0:
        return False
    global price
    price += coffees[n].price

def remove_from_order(selection):
    global price
    console = Console()
    rtab = Table(title="☕ Current selection", box = box.ROUNDED, caption="type index to remove from order\n[0] to exit")

    #Check if all values are equal to 0
    S = all(value == 0 for value in selection.values())

    if (S == True) or (not selection):
        return -1

    rtab.add_column("Index", style="bold	#87CEEB", justify="center")
    rtab.add_column("Name", style="bold italic #9966cc", justify="center")
    rtab.add_column("Quantity", style="bold	#87CEEB", justify="center")

    #Get currently selected coffees
    select = {key: value for key, value in selection.items() if value > 0}
    names = list(select.keys())

    for i in range(len(names)):
        rtab.add_row(str(i+1),names[i],str(selection[names[i]]))

    console.print(rtab)

    while True:
        try:
            r = int(input("Enter: "))
            if r == 0:
                return False

            cls = get_class(names[r-1].lower())
            price -= cls.price

            return names[r-1]
        except ValueError:
            console.print("Invalid usage ", style="bold red", end="")
            console.print("Please write index of item you want to remove from order", style="italic")
        except IndexError:
            console.print("Invalid usage ", style="bold red", end="")
            console.print("Please write correct index of item you want to remove", style="italic")

def get_class(class_name):
    if not class_name:
        return None
    return globals()[class_name]


def validator(number):
    n = number
    sum = 0
    c = 0
    while (n > 1):
        if (c % 2 != 0):
            x = (n % 10) * 2
            if x > 9:
                sum += x % 10
                sum += x // 10
            else:
                sum += x
        else:
            sum += n % 10
        n = n // 10
        c += 1
    if sum % 10 == 0:
        first = number
        digits = 2
        while first > 100:
            first = first // 10
            digits += 1

        # Checking how many digits, what are first digits and is calculation correct
        if ((digits == 15) and ((first == 34) or (first == 37))):
            return "AMEX"
        elif ((digits == 16) and ((first > 50) and (first < 56))):
            return "MASTERCARD"
        elif ((digits == 13 or digits == 16) and (first > 39 and first < 50)):
            return "VISA"
        else:
            return False
    return False

def print_receipt(select, receipt):
    console = Console()

    items = {name:value for name,value in select.items() if value!=0}
    names = list(items.keys())

    n = 0.2
    console.print("\n[bold underline]Receipt[/bold underline]")
    time.sleep(n)
    console.print(f"[magenta]Order Number:[/magenta] {receipt.order_number}")
    time.sleep(n)
    console.print(f"[magenta]Customer Name:[/magenta] {receipt.name}")
    time.sleep(n)
    console.print("_______________________________________")
    time.sleep(n)
    console.print("[cyan]Item[/cyan]                  [cyan]QTY[/cyan]         [cyan]Price[/cyan]")
    for i in range(len(names)):
        cls = get_class(names[i].lower())

        time.sleep(n)
        print(f"{names[i].ljust(22)} {str(items[names[i]]).ljust(10)} ${cls.price*items[names[i]]:.2f}")
    time.sleep(n)
    console.print("_______________________________________")
    time.sleep(n)
    console.print(f"\n[bold]Total Price:[/bold]                      [bold green]${receipt.total:.2f}[/bold green]")
    time.sleep(n)
    console.print("\n\nWe are preparing your order!\n", style="italic bold")

    time.sleep(n)
    print("     ( (")
    time.sleep(n)
    print("      ) )")
    time.sleep(n)
    print("  .........")
    time.sleep(n)
    print("  |       |]")
    time.sleep(n)
    print("  \       /")
    time.sleep(n)
    print("   `-----'")
    time.sleep(n)
    console.print("Thank you and visit us again!", style="cyan")



if __name__ == "__main__":
    main()
