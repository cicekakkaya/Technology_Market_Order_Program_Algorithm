# Technology Shop Order Program

class ProductManager:
    """Handles product-related operations: validation, addition, deletion, and display."""
    def __init__(self):
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
        if category and category in self.products:
            print(f"\n{'='*60}\n{category.upper()}\n{'='*60}")
            for item in self.products[category]:
                print(f"Code: {item['ItemCode']:<6} | {item['Description']:<45} | ${item['Price']:>7.2f}")
        else:
            for cat, items in self.products.items():
                print(f"\n{'='*60}\n{cat.upper()}\n{'='*60}")
                for item in items:
                    print(f"Code: {item['ItemCode']:<6} | {item['Description']:<45} | ${item['Price']:>7.2f}")

    def validate_item_code(self, item_code):
        item_code = item_code.upper()
        return any(item["ItemCode"] == item_code for items in self.products.values() for item in items)

    def get_item_by_code(self, item_code):
        item_code = item_code.upper()
        for category, items in self.products.items():
            for item in items:
                if item["ItemCode"] == item_code:
                    return {"category": category, **item}
        return None

class ShoppingCart:
    """Manages the current customer's selections and calculations."""
    def __init__(self, product_manager):
        self.product_manager = product_manager
        self.cart_items = []
        self.device_count = 0 

    def add_item(self, item_code, quantity=1):
        item = self.product_manager.get_item_by_code(item_code)
        if item:
            self.cart_items.append({
                "ItemCode": item_code,
                "Description": item["Description"],
                "Price": item["Price"],
                "Category": item["category"],
                "Quantity": quantity
            })
            if item["category"] in ["Phones", "Tablets"]:
                self.device_count += 1

    def calculate_subtotal(self):
        return sum(item["Price"] * item["Quantity"] for item in self.cart_items)

    def calculate_discount(self):
        if self.device_count <= 1:
            return 0.0
        
        discount = 0.0
        device_counter = 0
        for item in self.cart_items:
            if item["Category"] in ["Phones", "Tablets"]:
                device_counter += 1
                if device_counter > 1: # 10% off the 2nd device onwards
                    discount += (item["Price"] * item["Quantity"]) * 0.10
        return discount

    def calculate_total(self):
        return self.calculate_subtotal() - self.calculate_discount()

    def print_receipt(self):
        print("\n" + "="*70)
        print(" "*25 + "FINAL RECEIPT")
        print("="*70)
        if not self.cart_items:
            print("Cart is empty.")
            return

        for item in self.cart_items:
            print(f"{item['ItemCode']:<6} | {item['Description']:<40} | ${item['Price']:>7.2f} x{item['Quantity']}")
        
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        print("-" * 70)
        print(f"{'Subtotal:':<57} ${subtotal:>10.2f}")
        if discount > 0:
            print(f"{'Total Discount (10% off addtl. devices):':<57} -${discount:>9.2f}")
        print(f"{'TOTAL:':<57} ${subtotal - discount:>10.2f}")
        print("="*70)

class MobileShop:
    """Orchestrates the shop operations and user flow."""
    def __init__(self):
        self.product_manager = ProductManager()

    def select_device(self):
        print("\n--- SELECT YOUR DEVICE ---")
        print("1. Phones\n2. Tablets")
        choice = input("Choose device type (1 or 2): ")
        category = "Phones" if choice == "1" else "Tablets" if choice == "2" else None
        
        if not category:
            print("Invalid choice.")
            return None

        self.product_manager.display_products(category)
        device_code = input(f"\nEnter {category[:-1]} code: ").upper()
        if self.product_manager.validate_item_code(device_code):
            return device_code
        print(f"Error: Invalid code {device_code}")
        return None

    def process_device_order(self, cart):
        device_code = self.select_device()
        if not device_code: return False
        
        cart.add_item(device_code)

        # SIM Card
        self.product_manager.display_products("SIM cards")
        sim = input("\nEnter SIM card code: ").upper()
        cart.add_item(sim if self.product_manager.validate_item_code(sim) else "SMNO")

        # Case
        self.product_manager.display_products("Cases")
        case = input("\nEnter case code: ").upper()
        cart.add_item(case if self.product_manager.validate_item_code(case) else "CSST")

        # Chargers
        self.product_manager.display_products("Chargers")
        if input("Add Car charger? (y/n): ").lower() == 'y': cart.add_item("CGCR")
        if input("Add Home charger? (y/n): ").lower() == 'y': cart.add_item("CGHM")
        
        return True

    def customer_shopping_session(self):
        print("\n" + "="*70 + "\n" + " "*20 + "WELCOME TO MOBILE SHOP\n" + "="*70)
        cart = ShoppingCart(self.product_manager)
        
        while True:
            if self.process_device_order(cart):
                subtotal = cart.calculate_subtotal()
                discount = cart.calculate_discount()
                
                print(f"\n--- ORDER UPDATE ---")
                print(f"Devices in cart: {cart.device_count}")
                print(f"Subtotal: ${subtotal:.2f}")
                if discount > 0:
                    print(f"Applied Discount: -${discount:.2f}")
                    print(f"New Total: ${subtotal - discount:.2f}")
                else:
                    print("No discount applied (Buy 2+ devices for 10% off additional units)")
            
            another = input("\nWould you like to purchase another device? (y/n): ").lower()
            if another != 'y':
                break

        if cart.cart_items:
            if input("\nConfirm purchase? (y/n): ").lower() == "y":
                cart.print_receipt()
            else:
                print("Order discarded.")

    def main_menu(self):
        while True:
            print("\n" + "="*50 + "\n" + " "*10 + "MOBILE SHOP MAIN MENU\n" + "="*50)
            print("1. Customer Shopping\n2. Exit")
            choice = input("\nEnter your choice (1-2): ")
            if choice == "1": self.customer_shopping_session()
            elif choice == "3" or choice == "2": break

if __name__ == "__main__":
    shop = MobileShop()
    shop.main_menu()