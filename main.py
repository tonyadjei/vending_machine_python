from functionalities import user, admin, validate_number
from data import ADMIN_NAME, ADMIN_PASSWORD
import sys

def main():
    while True:
        print("Welcome to the vending machine \n ----------------------------- \nYou can operate this machine with the following roles: \n1. Admin \n2. User\n")
        print("Enter '0' to quit the application")
        option = input("Select an option: ")
        print()
        if validate_number(option):
            if option == "1":
                admin_name = input("Enter admin username: ")
                admin_password = input("Enter admin password: ")
                print()
                if admin_name == ADMIN_NAME and admin_password == ADMIN_PASSWORD:
                    admin()
                else:
                    print("Invalid credentials: You entered the wrong username and/or password.")
            elif option == "2":
                user()
            elif option == "0":
                sys.exit(0)
            else:
                print("Invalid input <{}>: Enter a value of '1' or '2'.".format(option))
        else:
            print("Invalid input <{}>: Enter a value of '1' or '2'.".format(option))

# run main program
main()