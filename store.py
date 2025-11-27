import csv
from datetime import datetime

#ზოგადი პროდუქტის ლოგიკა, რომელიც ინახავს სახელს, ფასს და რაოდენობას სტოკში.
#ასევე მიწერია ლოგიკა, რომ მინუს ციფრით ვერ შეძლებენ პროდუქტის აღებას და აუცილებლად უნდა იყოს დადებითი რიცხვი შეყვანილი
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def reduce_quantity(self, amount):
        if amount <= 0:
            print("Amount must be positive.")
            return False
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False

    #აბტუნებს წასაკითხ სტრინგს, მაგალითად bread - 30 left
    def __str__(self):
        return f"{self.name} - {self.quantity} left"

#პურის კლასი, რომელიც ზემოთხსენებული პროდუქტის კლასიდან იღებს მემკვიდრეობას.
class Bread(Product):
    def __init__(self, quantity):
        super().__init__("bread", 1.5, quantity)

#ანალოგიურია კვერცხის კლასიც, თუმცა გავუკეთე თავისი ლოგიკა, ანუ ფერენთ მეთოდი გადავწერე და დავუწერე custom logic
#აქაც ვბლოკავ არასწორ ინფუთს ანუ 0 ან 0ზე ნაკლები ვერ იქნება და აუცილებლად დადებითი ციფრი უნდა იყოს შეყვანილი
#სპეციალურად არის დაწერილი რო პაკეტებში იყოს ნაჩვენები
class Eggs(Product):
    def __init__(self, packs):
        super().__init__("eggs", 6, packs)

    def reduce_quantity(self, packs_requested):
        if packs_requested <= 0:
            print("Amount must be positive.")
            return False
        if packs_requested <= self.quantity:
            self.quantity -= packs_requested
            return True
        return False
#ანალოგიური კოდია მემკვიდრეობას იღებს პროდუქტის კლასიდან
class Oil(Product):
    def __init__(self, quantity):
        super().__init__("oil", 12, quantity)
#მარილზეც ანალოგიური
class Salt(Product):
    def __init__(self, grams):
        super().__init__("salt", 2.5, grams)

#მაღაზიის კლასი, რომელიც ამენეჯებს სტოკს (რაოდენობას) და გაყიდვებს.

class Store:
    #ვინახავ ინფორმაციას csv ფაილში
    def __init__(self, stock_file="store_stock.csv"):
        self.stock_file = stock_file
        self.products = {}
        self.load_stock()
    
    #ვიღებ ინფორმაციას csv ფაილიდან, ან თუ არ არის csv ფაილი, გაწერილი მაქვს default მონაცემები, რომელიც საწყის ფაზაში ექმნება.
    #თუ პროგრამას ერთხელ გავუშვებთ ინფორმაცია შეინახება csv ფაილში და შემდგომ იქიდან წამოიღებს ინფორმაციას
    def load_stock(self):
        try:
            with open(self.stock_file, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row["product"]
                    price = float(row["price"])
                    quantity = float(row["quantity"])
                    if name == "bread":
                        self.products["bread"] = Bread(quantity)
                    elif name == "eggs":
                        self.products["eggs"] = Eggs(quantity)
                    elif name == "oil":
                        self.products["oil"] = Oil(quantity)
                    elif name == "salt":
                        self.products["salt"] = Salt(quantity)
        except FileNotFoundError:
            self.products = {
                "bread": Bread(50),
                "eggs": Eggs(15),  # 15 პაკეტი = 150 კვერცხი
                "oil": Oil(20),
                "salt": Salt(2000),  # დაწერილი მაქვს გრამებში
            }
            self.save_stock()

    #ეს ფუნქცია ააფდეითებს csv ფაილს, ხსნის csv ფაილს წერის მოდში და ძველ დატას გადააკეთებს ახალი დატით
    def save_stock(self):
        with open(self.stock_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["product", "price", "quantity"])
            for product in self.products.values():
                writer.writerow([product.name, product.price, product.quantity])

    #ამ ფუნქციას გამოაქვს პროდუქტები ტერმინალში და გვაჩვენებს, თუ რა პროდუქტებია დარჩენილი სტოკში
    def show_products(self):
        print("\nAvailable products:")
        for p in self.products.values():
            if p.name == "eggs":
                print(f"{p.name} - {p.quantity*10} eggs ({p.quantity} packs) -- {p.price} GEL per pack")
            elif p.name == "salt":
                print(f"{p.name} - {p.quantity} grams -- {p.price} GEL per 100g")
            else:
                print(f"{p.name} - {p.quantity} units -- {p.price} GEL per unit")

    
    #მთლიანი ყიდვის ლოგიკა:
    def buy_product(self, cart, product_name, amount):
        if product_name not in self.products: #თუ პროდუქტის სახელი არ იძებნება გამოაქვს product not found და აჩერებს ყიდვის პროცესს
            print("Product not found.")
            return False

        product = self.products[product_name]

        if amount <= 0:
            print("Amount must be positive.") #ამოწმებს მინუს ან 0 იან amount-ს, რაც აჩერებს ყიდვის პროცესს და არ გვაძლევს საშუალებას მინუს ნივთის აღების.
            return False

        # ამოწმებს სტოკში საკმარისია თუ არა, პრინტავს 1 პაკეტში რამდენი კვერცხიც შედის
        if product_name == "eggs":
            if amount > product.quantity:
                print(f"Only {product.quantity} packs available. Enter a smaller number.")
                return False
            cart[product_name] = cart.get(product_name, 0) + amount
            product.reduce_quantity(amount)
            print(f"{amount*10} eggs added to cart ({amount} packs).")
            return True
            

        if product_name == "salt":
            if amount > product.quantity:
                print(f"Only {product.quantity} grams available. Enter a smaller number.")
                return False
            cart[product_name] = cart.get(product_name, 0) + amount
            product.reduce_quantity(amount)
            print(f"{amount} grams of salt added to cart.")
            return True

        if amount > product.quantity:
            print(f"Only {product.quantity} units available. Enter a smaller number.")
            return False
        cart[product_name] = cart.get(product_name, 0) + amount
        product.reduce_quantity(amount)
        print(f"{amount} {product_name} added to cart.")
        return True

def main():
    store = Store() #ქმნის store ობჯექთს რომელიც ალოადებს სტოკს csv დან ან დეფაულტად რაც არი გაწერილი იღებს მაქრდან
    cart = {} #ცარიელი კალათა

    print("Welcome to the Rodrigo Store!")
    while True:
        store.show_products()
        print("\nEnter product to buy (or 'done' to finish):")
        choice = input("> ").lower()
        if choice == "done":
            break
        if choice not in store.products:
            print("Invalid product. Try again.")
            continue
        try:
            if choice == "salt":
                amount = float(input(f"Enter grams of {choice}: "))
            elif choice == "eggs":
                amount = int(input(f"Enter number of packs of {choice} (1 pack = 10 eggs): "))
            else:
                amount = int(input(f"Enter number of {choice} to buy: "))
        except ValueError:
            print("Invalid number. Try again.")
            continue

        store.buy_product(cart, choice, amount)

    if not cart:
        print("No products purchased.")
        return

    total = 0
    print("\nYour cart:")
    for name, amount in cart.items():
        product = store.products[name]
        if name == "eggs":
            count = amount * 10
            price = amount * product.price
            print(f"{amount} packs ({count} eggs) {name} -- {price} GEL")
        elif name == "salt":
            price = amount / 100 * product.price
            print(f"{amount} grams {name} -- {price:.2f} GEL")
        else:
            price = amount * product.price
            print(f"{amount} {name} -- {price:.2f} GEL")
        total += price

    print("----------------------------")
    print(f"Total price -- {total:.2f} GEL")

    while True:
        try:
            money = float(input(f"Enter money to pay ({total:.2f} GEL): "))
            if money < total:
                print("Not enough money. Try again.")
            else:
                change = money - total
                print(f"Payment accepted. Your change: {change:.2f} GEL")
                break
        except ValueError:
            print("Invalid input. Enter a number.")


    #ქმნის ჩეკს
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"receipt_{now}.txt"
    with open(filename, "w") as f:
        f.write(f"Receipt at {datetime.now()}\n")
        f.write("----------------------------\n")
        for name, amount in cart.items():
            product = store.products[name]
            if name == "eggs":
                count = amount * 10
                price = amount * product.price
                f.write(f"{amount} packs ({count} eggs) {name} -- {price} GEL\n")
            elif name == "salt":
                price = amount / 100 * product.price
                f.write(f"{amount} grams {name} -- {price:.2f} GEL\n")
            else:
                price = amount * product.price
                f.write(f"{amount} {name} -- {price:.2f} GEL\n")
        f.write("----------------------------\n")
        f.write(f"Total price -- {total:.2f} GEL\n")
        f.write(f"Paid: {money:.2f} GEL\n")
        f.write(f"Change: {change:.2f} GEL\n")
    print(f"Receipt saved to {filename}")

    store.save_stock()

if __name__ == "__main__":
    main()
