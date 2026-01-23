


"""
ProductManager class handles all product-related operations including

validation, addition, deletion, and displaying product information.

"""

class ProductManager:

    def __init__(self):

        """Initialize the product database with available items"""

        self.products = {

            "Phones": [

                {"ItemCode": "BPCM", "Description": "Compact", "Price": 29.99},

                {"ItemCode": "BPSH", "Description": "Clam shell", "Price": 49.99},

                {"ItemCode": "RPSS", "Description": "Robo phone - 5inch 64GB memory", "Price": 199.99},

                {"ItemCode": "RPLL", "Description": "Robo phone - 6inch 256GB memory", "Price": 499.99},

                {"ItemCode": "YPLS", "Description": "Y-phone standard 6 inch 64GB memory", "Price": 549.99},

                {"ItemCode": "YPLL", "Description": "Y-phone deluxe 6 inch 256GB memory", "Price": 649.99}

            ],

            "Tablets": [

                {"ItemCode": "RTMS", "Description": "RoboTab - 8 inch screen 64GB memory", "Price": 149.99},

                {"ItemCode": "RTML", "Description": "RoboTab - 10 inch screen 128GB memory", "Price": 299.99},

                {"ItemCode": "YTLM", "Description": "Y-tab standard - 10 inch screen 128GB memory", "Price": 499.99},

                {"ItemCode": "YTLL", "Description": "Y-tab deluxe - 10 inch screen 256GB memory", "Price": 599.99}

            ],

            "SIM cards": [

                {"ItemCode": "SMNO", "Description": "Sim free (no SIM card)", "Price": 0.00},

                {"ItemCode": "SMPG", "Description": "Pay as you go (with SIM card)", "Price": 9.99}

            ],

            "Cases": [

                {"ItemCode": "CSST", "Description": "Standard", "Price": 0.00},

                {"ItemCode": "CSLX", "Description": "Luxury", "Price": 50.00}

            ],

            "Chargers": [

                {"ItemCode": "CGCR", "Description": "Car", "Price": 19.99},

                {"ItemCode": "CGHM", "Description": "Home", "Price": 15.99}

            ]

        }

   

    def display_products(self, category=None):

        """

        Display all products or products from a specific category

       

        Args:

            category (str): Optional category name to display specific products

        """

        if category and category in self.products:

            print(f"\n{'='*60}")

            print(f"{category.upper()}")

            print(f"{'='*60}")

            for item in self.products[category]:

                print(f"Code: {item['ItemCode']:<6} | {item['Description']:<45} | ${item['Price']:>7.2f}")

        else:

            for cat, items in self.products.items():

                print(f"\n{'='*60}")

                print(f"{cat.upper()}")

                print(f"{'='*60}")

                for item in items:

                    print(f"Code: {item['ItemCode']:<6} | {item['Description']:<45} | ${item['Price']:>7.2f}")

   

    def validate_item_code(self, item_code):

        """

        Validate if an item code exists in the product database

       

        Args:

            item_code (str): The item code to validate

           

        Returns:

            bool: True if item code exists, False otherwise

        """

        item_code = item_code.upper()

        for category, items in self.products.items():

            for item in items:

                if item["ItemCode"] == item_code:

                    return True

        return False

   

    def get_item_by_code(self, item_code):

        """

        Retrieve item details by item code

       

        Args:

            item_code (str): The item code to search for

           

        Returns:

            dict: Item information or None if not found

        """

        item_code = item_code.upper()

        for category, items in self.products.items():

            for item in items:

                if item["ItemCode"] == item_code:

                    return {"category": category, **item}

        return None

   

    def add_new_product(self):

        """

        Add a new product entry with validation

        Prompts user for item code, description, price, and category

        """

        print("\n--- ADD NEW PRODUCT ---")

        new_item_code = input("Enter the new item code: ").upper()

       

        # Check if item code already exists

        if self.validate_item_code(new_item_code):

            print(f"Error: Item code {new_item_code} already exists. Product not added.")

            return

       

        # Get product details

        description = input("Enter the product description: ")

       

        # Validate price input

        try:

            price = round(float(input("Enter the product price: $")), 2)

            if price < 0:

                print("Error: Price cannot be negative. Product not added.")

                return

        except ValueError:

            print("Error: Invalid price format. Please enter a valid number.")

            return

       

        # Get and validate category

        print("\nAvailable categories:", ", ".join(self.products.keys()))

        category = input("Enter the product category: ").strip()

       

        # Capitalize first letter of each word for matching

        category = " ".join(word.capitalize() for word in category.split())

       

        if category in self.products:

            # Add new product to the category

            self.products[category].append({

                "ItemCode": new_item_code,

                "Description": description,

                "Price": price

            })

            print(f"\nSuccess! New product added to {category} category.")

            print(f"Item code {new_item_code} is now valid.")

        else:

            print(f"Error: Category '{category}' is invalid. Product not added.")

   

    def delete_item(self):

        """

        Delete an item from the product database by item code

        Allows multiple deletions until user chooses to exit

        """

        print("\n--- DELETE PRODUCT ---")

       

        while True:

            item_code = input("Enter item code to delete (or 'exit' to quit): ").upper()

           

            if item_code.lower() == 'exit':

                print("Exiting delete mode.")

                break

           

            # Validate item code exists

            if not self.validate_item_code(item_code):

                print(f"Error: Item code {item_code} does not exist. Deletion cancelled.")

                break

           

            # Find and delete the item

            found = False

            for category, items in self.products.items():

                for item in items[:]:  # Create a copy to safely remove items

                    if item["ItemCode"] == item_code:

                        items.remove(item)

                        print(f"Success! Item {item_code} deleted from {category} category.")

                        found = True

                        break

                if found:

                    break

   

    def count_total_items(self):

        """

        Count and display the total number of items in the product database

       

        Returns:

            int: Total number of items

        """

        total = sum(len(items) for items in self.products.values())

        print(f"\nTotal number of items in database: {total}")

        return total





class ShoppingCart(ProductManager):

    """

    ShoppingCart class manages customer purchases including item selection,

    discount calculation, and receipt generation.

    """

   

    def __init__(self, product_manager):

        """

        Initialize shopping cart with reference to product manager

       

        Args:

            product_manager (ProductManager): Instance of ProductManager class

        """

        self.product_manager = product_manager

        self.cart_items = []

        self.device_count = 0  # Track number of devices for discount

   

    def add_item(self, item_code, quantity=1):

        """

        Add an item to the cart

        Args:

            item_code (str): The item code to add

        """

        item = self.product_manager.get_item_by_code(item_code)


        self.cart_items.append({
            "ItemCode": item_code,

            "Description": item["Description"],

            "Price": item["Price"],

            "Category": item["category"],
            "Quantity": quantity

        })

            # Track devices for discount calculation

        if item["category"] in ["Phones", "Tablets"]:

                self.device_count += 1



    def calculate_subtotal(self):

        """

        Calculate subtotal before discounts

       

        Returns:

            float: Subtotal amount

        """

        return sum(item["Price"] * item["Quantity"] for item in self.cart_items)

   

    def calculate_discount(self):

        """

        Calculate 10% discount for additional devices (2nd device onwards)

       

        Returns:

            float: Discount amount

        """

        if self.device_count <= 1:

            return 0.0

       

        # Apply 10% discount to additional devices

        discount = 0.0

        device_counter = 0

       

        for item in self.cart_items:

            if item["Category"] in ["Phones", "Tablets"]:

                device_counter += 1

                if device_counter > 1:  # Discount starts from 2nd device

                    discount += item["Price"] * item["Quantity"] * 0.10

            return discount

   

    def calculate_total(self):

        """

        Calculate final total after applying discounts

       

        Returns:

            float: Final total amount

        """

        subtotal = self.calculate_subtotal()

        discount = self.calculate_discount()

        return subtotal - discount

   

    def print_receipt(self):

        """

        Print detailed receipt with all items, prices, and totals

        """

        print("\n" + "="*70)

        print(" "*25 + "RECEIPT")

        print("="*70)

       

        if not self.cart_items:

            print("Cart is empty.")
        else:
            pass


        # Print items

        for item in self.cart_items:

            print(f"{item['ItemCode']:<6} | {item['Description']:<40} | ${item['Price']:>7.2f} x{item['Quantity']}")

       

        print("-"*70)

       

        # Calculate amounts

        subtotal = self.calculate_subtotal()

        discount = self.calculate_discount()

        total = self.calculate_total()

       

        # Print totals

        print(f"{'Subtotal:':<57} ${subtotal:>10.2f}")

       

        if discount > 0:

            print(f"{'Discount (10% off additional devices):':<57} -${discount:>9.2f}")

            print(f"{'Amount Saved:':<57} ${discount:>10.2f}")

       

        print(f"{'TOTAL:':<57} ${total:>10.2f}")

        print("="*70)





class MobileShop(ShoppingCart, ProductManager):

    """

    Main class that orchestrates the mobile shop operations

    including customer interaction and order processing.

    """

   

    def __init__(self):

        """Initialize the mobile shop with product manager"""

        self.product_manager = ProductManager()


    def select_device(self):

        """

        Allow customer to select a phone or tablet

       

        Returns:

            str: Selected device item code or None

        """

        print("\n--- SELECT YOUR DEVICE ---")

        print("1. Phones")

        print("2. Tablets")

       

        choice = input("Choose device type (1 or 2): ")

       

        if choice == "1":

            self.product_manager.display_products("Phones")

            device_code = input("\nEnter phone code: ").upper()

        elif choice == "2":

            self.product_manager.display_products("Tablets")

            device_code = input("\nEnter tablet code: ").upper()

        else:

            print("Invalid choice.")

            return None

       

        # Validate device code

        if self.product_manager.validate_item_code(device_code):

            return device_code

        else:

            print(f"Error: Invalid device code {device_code}")

            return None

   

    def select_sim_card(self):

        """

        Allow customer to choose SIM card option (for phones)

       

        Returns:

            str: Selected SIM card item code

        """

        print("\n--- SELECT SIM CARD OPTION ---")

        self.product_manager.display_products("SIM cards")

       

        sim_code = input("\nEnter SIM card code: ").upper()

       

        if self.product_manager.validate_item_code(sim_code):

            return sim_code

        else:

            print("Invalid SIM card code. Defaulting to SIM Free.")

            return "SMNO"

   

    def select_case(self):

        """

        Allow customer to choose a case

       

        Returns:

            str: Selected case item code

        """

        print("\n--- SELECT CASE ---")

        self.product_manager.display_products("Cases")

       

        case_code = input("\nEnter case code: ").upper()

       

        if self.product_manager.validate_item_code(case_code):

            return case_code

        else:

            print("Invalid case code. Defaulting to Standard.")

            return "CSST"

   

    def select_chargers(self):

        """

        Allow customer to choose chargers (none, one, or both)

       

        Returns:

            list: List of selected charger item codes

        """

        print("\n--- SELECT CHARGERS ---")

        self.product_manager.display_products("Chargers")

       

        chargers = []

       

        car_charger = input("\nDo you want a Car charger? (y/n): ").lower()

        if car_charger == "y":

            chargers.append("CGCR")

       

        home_charger = input("Do you want a Home charger? (y/n): ").lower()

        if home_charger == "y":

            chargers.append("CGHM")

       

        return chargers

   

    def process_device_order(self, cart):

        """

        Process a complete device order with all accessories

       

        Args:

            cart (ShoppingCart): The shopping cart to add items to

           

        Returns:

            bool: True if order processed successfully

        """

        # Select device

        while True:

            device_code = self.select_device()

            if not device_code:

                return False

       

            cart.add_item(device_code)


            # Select SIM card

            sim_code = self.select_sim_card()

            cart.add_item(sim_code)

       

            # Select case

            case_code = self.select_case()

            cart.add_item(case_code)

       

            # Select chargers

            charger_codes = self.select_chargers()

            for charger in charger_codes:

                cart.add_item(charger)


            break

    def customer_shopping_session(self):

        """

        Main shopping session allowing multiple device purchases

        Implements Task 1, 2, and 3 from the requirements

        """

        print("\n" + "="*70)

        print(" "*20 + "WELCOME TO MOBILE SHOP")

        print("="*70)

       

        cart = ShoppingCart(self.product_manager)

       
        # First device purchase


        if not self.process_device_order(cart):

            print("Order cancelled.")
        else:
            pass


        # Show current total after first device

        print(f"\nCurrent total: ${cart.calculate_subtotal():.2f}")

       

        # Offer additional devices (Task 2)

        print("Select another device? (y/n)")

        while True:

            another = input("\nWould you like to purchase another device? (y/n): ").lower()

            if another == 'y':

                # Second device purchase

                print("\n" + "="*70)

                print(" "*15 + "SPECIAL DISCOUNT OFFER!")

                print("="*70)

                print(f"You have purchased {cart.device_count} devices!")

                print("You qualify for 10% discount on additional devices (2nd device onwards)")

                discount_amount = cart.calculate_discount()

                print(f"Your discount: ${discount_amount:.2f}")

                print(f"Amount you save: ${discount_amount:.2f}")  

                # Show running total after each device

                print(f"\nCurrent total: ${cart.calculate_subtotal():.2f}")


            elif another != 'y':

                print("\n" + "="*70)

                print(f"\nCurrent total: ${cart.calculate_subtotal():.2f}")

                print("Thank you for your purchase!")
                break

            else:

                print("Invalid choice. Please try again.")
                break
            break
        

        # After all devices are selected, show discount offer (Task 3)


        # Payment confirmation

        confirm = input("\nConfirm purchase? (y/n): ").lower()

        if confirm == "y":

            print("\nThank you for your purchase!")

            print("Your order has been confirmed.")

        else:

            print("\nOrder cancelled.")


       

        # Print final receipt with discount applied

        cart.print_receipt()



    def admin_menu(self):

        """

        Admin menu for managing products (add, delete, view)

        """

        while True:

            print("\n" + "="*50)

            print(" "*15 + "ADMIN MENU")

            print("="*50)

            print("1. View all products")

            print("2. Add new product")

            print("3. Delete product")

            print("4. Count total items")

            print("5. Exit admin menu")

           

            choice = input("\nEnter your choice (1-5): ")

           

            if choice == "1":

                self.product_manager.display_products()

            elif choice == "2":

                self.product_manager.add_new_product()

            elif choice == "3":

                self.product_manager.delete_item()

            elif choice == "4":

                self.product_manager.count_total_items()

            elif choice == "5":

                print("Exiting admin menu...")

                break

            else:

                print("Invalid choice. Please try again.")

   

    def main_menu(self):

        """

        Main menu for the application

        Allows switching between customer shopping and admin functions

        """

        while True:

            print("\n" + "="*50)

            print(" "*10 + "MOBILE SHOP MAIN MENU")

            print("="*50)

            print("1. Customer Shopping")

            print("2. Admin Panel")

            print("3. Exit")

           

            choice = input("\nEnter your choice (1-3): ")

           

            if choice == "1":

                self.customer_shopping_session()

            elif choice == "2":

                self.admin_menu()

            elif choice == "3":

                print("\nThank you for using Mobile Shop System!")

                print("Goodbye!")

                break

            else:

                print("Invalid choice. Please try again.")


# Main program execution

if __name__ == "__main__":

    shop = MobileShop()

    shop.main_menu()