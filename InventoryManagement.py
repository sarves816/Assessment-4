class Inventory:

    def __init__(self):
        self.warehouses = {
            "A": {},
            "B": {},
            "C": {}
        }
        self.suppliers = {}

    def add_product(self, warehouse, product, quantity):
        if quantity < 0:
            return "Invalid quantity"

        self.warehouses[warehouse][product] = (
            self.warehouses[warehouse].get(product, 0) + quantity
        )

        return "Product added"

    def remove_product(self, warehouse, product, quantity):
        if product not in self.warehouses[warehouse]:
            return "Invalid product"

        if quantity < 0:
            return "Invalid quantity"

        if self.warehouses[warehouse][product] < quantity:
            return "Insufficient inventory"

        self.warehouses[warehouse][product] -= quantity

        return "Product removed"

    def transfer(self, source, destination, product, quantity):
        result = self.remove_product(source, product, quantity)

        if result != "Product removed":
            return result

        self.add_product(destination, product, quantity)

        return "Stock transferred"

    def reorder(self, warehouse, product, threshold=10, amount=50):
        if self.warehouses[warehouse].get(product, 0) < threshold:
            self.add_product(warehouse, product, amount)
            return "Reordered"

        return "Stock sufficient"

    def add_supplier(self, name, product):
        self.suppliers[name] = product
        return "Supplier added"

    def low_stock(self, warehouse, threshold=10):
        return [
            product
            for product, quantity in self.warehouses[warehouse].items()
            if quantity < threshold
        ]

    def select_warehouse(self, product):
        available = [
            warehouse
            for warehouse in self.warehouses
            if self.warehouses[warehouse].get(product, 0) > 0
        ]

        return available[0] if available else None

    def fulfill_order(self, product, quantity):
        warehouse = self.select_warehouse(product)

        if not warehouse:
            return "Insufficient inventory"

        if self.warehouses[warehouse][product] < quantity:
            return "Insufficient inventory"

        return self.remove_product(warehouse, product, quantity)


if __name__ == "__main__":
    inventory = Inventory()

    print(inventory.add_product("A", "Laptop", 20))
    print(inventory.add_product("B", "Laptop", 10))
    print(inventory.add_supplier("Supplier1", "Laptop"))

    print("Warehouse:", inventory.select_warehouse("Laptop"))

    print(inventory.transfer("A", "C", "Laptop", 5))

    print(inventory.reorder("B", "Laptop"))

    print(inventory.low_stock("A"))
