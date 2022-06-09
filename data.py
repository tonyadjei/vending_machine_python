from classes import Sweet, CoinCompartment

# CONSTANTS / GLOBAL VARIABLES
ADMIN_NAME = "admin"
ADMIN_PASSWORD = "12345"
USER_CREDIT = 0
USER_DEBIT = 0
SWEETS = []
COMPARTMENTS = []

# TEST DATA
sweet1 = Sweet(4.50, "Chocolate bar", 15)
sweet2 = Sweet(2.50, "Chewing gum", 25)
sweet3 = Sweet(1.50, "Water bottle", 10)
sweet4 = Sweet(6.50, "Butter biscuit", 20)
sweet5 = Sweet(0.03, "Orange drink", 5)

SWEETS.append(sweet1)
SWEETS.append(sweet2)
SWEETS.append(sweet3)
SWEETS.append(sweet4)
SWEETS.append(sweet5)

comp1 = CoinCompartment(0, 2)
comp2 = CoinCompartment(1, 1)
comp3 = CoinCompartment(2, 0.50)
comp4 = CoinCompartment(3, 0.20)
comp5 = CoinCompartment(4, 0.10)
comp6 = CoinCompartment(5, 0.05)

COMPARTMENTS.append(comp1)
COMPARTMENTS.append(comp2)
COMPARTMENTS.append(comp3)
COMPARTMENTS.append(comp4)
COMPARTMENTS.append(comp5)
COMPARTMENTS.append(comp6)