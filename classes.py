# CLASSES
class Sweet:
    def __init__(self, price, label, quantity):
        self.price = price
        self.label = label
        self.quantity = quantity

    def __str__(self):
        return "{} ---------- Price: {} ---------- Quantity: {}".format(self.label, self.price, self.quantity if self.quantity > 0 else "Out of stock")

class CoinCompartment:
    capacity = 50
    def __init__(self, number, value, count=0):
        self.number = number
        # Coin/Compartment values are rounded off to 2 decimal places
        self.value = round(float(value), 2)
        self.count = count

    def __str__(self):
        return "Value: {} euros Number: {} Capacity: {}".format(self.value, self.number, self.capacity)

