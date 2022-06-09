from classes import Sweet, CoinCompartment
from data import COMPARTMENTS, SWEETS, USER_CREDIT, USER_DEBIT

# HELPER FUNCTIONS
def validate_number(number):
    try:
        float(number)
    except ValueError:
        return False
    else:
        return True

# FUNCTIONALITIES
# calculate the coins returned and change that cannot be returned as a credit note for next purchase
def calc_credit_and_balance(amount_to_be_returned):
    global USER_CREDIT
    global USER_DEBIT
    # get all the possible compartments for the initial 'amount_to_be_returned' value
    # NB 1: compartment values are floating points rounded to 2 decimal places
    # NB 2: 'amount_to_be_returned' is made a float and rounded off to 2 decimal places in order to match equality comparisons with compartment values
    possible_compartments = list(filter(lambda comp: comp.value <= round(float(amount_to_be_returned), 2), COMPARTMENTS))
    # check if initial amount_to_be_returned is smaller than all the compartment values
    if not len(possible_compartments):
        USER_CREDIT += amount_to_be_returned
        USER_DEBIT = 0
        return 0
    else:
        # a hash map that stores the change type/value and its count as well as the total change returned to the user
        change_map = {}
        total_change_returned = 0
        while len(possible_compartments) > 0:
            # get list of possible compartment values
            possible_compartments_values = [comp.value for comp in possible_compartments]
            change_returned = max(possible_compartments_values)
            try:
                change_map[str(change_returned) + " euros"] += 1
            except KeyError:
                change_map[str(change_returned) + " euros"] = 1
            total_change_returned += change_returned
            amount_to_be_returned -= change_returned
            possible_compartments = list(filter(lambda comp: comp.value <= round(float(amount_to_be_returned), 2), COMPARTMENTS))
        # add total_change_returned value to the change_map
        change_map["Total"] = round(float(total_change_returned), 2)
        # the new debit value is the total change returned by the vending machine
        # it may not be everything, but the remaining will be used as a credit note for the next purchase
        USER_DEBIT = total_change_returned
        # credit user with what remained to be returned
        USER_CREDIT += amount_to_be_returned
        return change_map

def checkout(sweet_name):
    global USER_CREDIT
    global USER_DEBIT
    sweet = list(filter(lambda sweet: sweet.label == sweet_name, SWEETS))
    sweet = sweet[0]
    # check if selected sweet is in stock
    if sweet.quantity == 0:
        print("Sorry, {} is out of stock. Please come back later or choose another sweet.".format(sweet.label))
        return False
    amount_to_pay = sweet.price
    amount_to_be_returned = 0
    # if there is credit from previous transaction, apply it for any new transaction
    if USER_CREDIT:
        print("Your CREDIT of {:.2f} euros has been applied.".format(USER_CREDIT))
        if amount_to_pay < USER_CREDIT:
            USER_CREDIT -= amount_to_pay
            amount_to_pay = 0
        else:
            # check if we can apply the credit to make a successful transaction
            # only apply the credit if the USER_DEBIT will be sufficient to see the transaction through
            if USER_DEBIT >= (amount_to_pay - USER_CREDIT):
                amount_to_pay -= USER_CREDIT
                USER_CREDIT = 0
    if USER_DEBIT < amount_to_pay:
        print("Amount TO PAY: {:.2f} Your CREDIT balance: {:.2f} Your DEBIT balance: {:.2f}.".format(amount_to_pay, USER_CREDIT, USER_DEBIT))
        print("Sorry, you have insufficient funds to perform this transaction. Please insert some coin(s).")
        return False
    elif USER_DEBIT >= amount_to_pay:
        amount_to_be_returned = USER_DEBIT - amount_to_pay
        USER_DEBIT -= amount_to_pay
        change_map = calc_credit_and_balance(amount_to_be_returned)
        sweet.quantity -= 1
        print("You have successfully purchased a {}".format(sweet.label))
        print("Amount PAID: {:.2f} Amount RETURNED: {} Your CREDIT balance: {:.2f} Your DEBIT balance: {:.2f}.".format(amount_to_pay, change_map, USER_CREDIT, USER_DEBIT))
        return True

def select_sweet():
    while True:
        if USER_CREDIT == 0 and USER_DEBIT == 0:
            print("You need to insert some coin(s) first.")
            break
        else:
            print("Available sweets to choose from:")
            print("-" * len("Available sweets to choose from:"))
            for sweet in SWEETS:
                print("- ", sweet)
            print()
            option = input("Enter the name of a sweet: ")
            if option in [sweet.label for sweet in SWEETS]:
                if checkout(option):
                    break                                                            
            else:
                print("Invalid input <{}>: Enter the name of any one of the available sweets.".format(option))

def manage_coin_compartment(compartment_number): 
    global COMPARTMENTS
    global USER_DEBIT
    # subtract 1 from user_option since comp number starts from 0
    compartment = list(filter(lambda comp: comp.number == int(compartment_number) - 1, COMPARTMENTS))
    compartment = compartment[0]
    if compartment.count >= 50:
        return False
    else:
        USER_DEBIT += compartment.value
        compartment.count += 1
        return True

def insert_coin():
    print("You have a total credit of {:.2f} euros.".format(USER_CREDIT))
    print("-" * len("You have a total credit of {:.2f} euros.".format(USER_CREDIT)))
    while True:
        print("You can insert the following coin types:")
        for index, compartment in enumerate(COMPARTMENTS):
            # add 1 to compartment.number in order to start listing from '1'
            print("{}. {:.2f} euros".format(index + 1, compartment.value))
        option = input("Enter '0' to exit the coin entry: ")
        if validate_number(option):
            # subtract 1 from user_option since comp number starts from 0
            if int(option) - 1 in [compartment.number for compartment in COMPARTMENTS]:
                if manage_coin_compartment(option):
                    print("Coin insertion successful: You have inserted a total of {:.2f} euros".format(USER_DEBIT))
                else:
                    print("Coin insertion unsuccessful: The capacity of the coin slot is full, please contact the admin or try another slot.")
            elif option == "0":
                break
            else:
                print("Invalid input <{}>: Select from the list of available coin types.".format(option))
        else:
            print("Invalid input <{}>: Select from the list of available coin types.".format(option))

def admin():
    global SWEETS
    global COMPARTMENTS
    while True:
        print("As an admin, you can: \nEnter '1' to add a new sweet. \nEnter '2' to add a new coin/compartment. \nEnter '0' to exit from this menu.\n")
        option = input("Select an option: ")
        print()
        if option == "1":
            while True:
                sweet_name = input("Enter sweet name: ")
                if sweet_name in [sweet.label for sweet in SWEETS]:
                    print("Invalid input <{}>: Sweet name already exists, type another name.".format(sweet_name))
                else:
                    break
            while True:
                sweet_price = input("Enter sweet price: ")
                if validate_number(sweet_price):
                    break
                else:
                    print("Invalid input <{}>: Enter a number value".format(sweet_price))
            while True:
                sweet_quantity = input("Enter quantity in stock: ")
                print()
                if validate_number(sweet_quantity):
                    break
                else:
                    print("Invalid input <{}>: Enter a number value".format(sweet_quantity))
            new_sweet = Sweet(float(sweet_price), sweet_name, int(sweet_quantity))
            SWEETS.append(new_sweet)
            print("You have successfully created a new Sweet - {}".format(new_sweet))
        elif option == "2":
            while True:
                coin_value = input("Enter coin value: ")
                if validate_number(coin_value):
                    # compare previous compartment value with user coin value; values must decline as compartment numbers increase
                    compartment_values = [comp.value for comp in COMPARTMENTS]
                    current_comp_value = min(compartment_values)
                    if float(coin_value) >= current_comp_value:
                        print("Invalid input <{}>: Enter a value lower than {} (previous compartment value)".format(coin_value, current_comp_value))
                    else:
                        break
                else:
                    print("Invalid input <{}>: Enter a floating point value".format(coin_value))
            while True:
                compartment_number = input("Enter the compartment number of the coin: ")
                print()
                if validate_number(compartment_number):
                    if int(compartment_number) in [comp.number for comp in COMPARTMENTS]:
                        print("Invalid input <{}>: This compartment number already exists. Please try again".format(compartment_number))
                    elif int(compartment_number) < 0:
                        print("Invalid input <{}>: Compartment numbers are from 0 upwards. Please try again".format(compartment_number))
                    else:
                        break
                else:
                    print("Invalid input <{}>: Enter an integer value.".format(compartment_number))
            new_compartment = CoinCompartment(int(compartment_number), float(coin_value))
            COMPARTMENTS.append(new_compartment)
            print("You have successfully created a new Compartment - {}".format(new_compartment))
        elif option == "0":
            break
        else:
            print("Invalid input: Enter a value of '1', '2' or '0'. ")

def user():
    while True:
        print("As a user, you can: \nEnter '1' to insert a coin. \nEnter '2' to choose a sweet. \nEnter '0' to exit from this menu.\n")
        option = input("Select an option: ")
        print()
        if option == "1":
            insert_coin()
        elif option == "2":
            select_sweet()
        elif option == "0":
            break
        else:
            print("Invalid input: Enter a value of '1', '2' or '0'. ")