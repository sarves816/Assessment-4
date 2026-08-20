import unittest

from InventoryManagement import Inventory


class InventoryQA(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()

        self.inventory.add_product("A", "Laptop", 20)
        self.inventory.add_product("B", "Phone", 5)

    def test_stock_availability(self):
        self.assertEqual(
            self.inventory.select_warehouse("Laptop"),
            "A"
        )

    def test_insufficient_inventory(self):
        self.assertEqual(
            self.inventory.remove_product("A", "Laptop", 100),
            "Insufficient inventory"
        )

    def test_warehouse_transfer(self):
        self.assertEqual(
            self.inventory.transfer("A", "C", "Laptop", 5),
            "Stock transferred"
        )

        self.assertEqual(
            self.inventory.warehouses["C"]["Laptop"],
            5
        )

    def test_concurrent_orders(self):
        self.assertEqual(
            self.inventory.remove_product("A", "Laptop", 15),
            "Product removed"
        )

        self.assertEqual(
            self.inventory.remove_product("A", "Laptop", 10),
            "Insufficient inventory"
        )

    def test_reorder_threshold(self):
        self.assertEqual(
            self.inventory.reorder("B", "Phone"),
            "Reordered"
        )

    def test_invalid_product(self):
        self.assertEqual(
            self.inventory.remove_product("A", "X", 1),
            "Invalid product"
        )

    def test_negative_inventory(self):
        self.assertEqual(
            self.inventory.add_product("A", "Laptop", -1),
            "Invalid quantity"
        )

    def test_multiple_warehouses(self):
        self.inventory.add_product("C", "Tablet", 10)

        self.assertEqual(
            self.inventory.select_warehouse("Tablet"),
            "C"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
