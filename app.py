import sys

class StockTrack:

    def __init__(self):
        self.menu()

    def menu(self):

        user_input = input(int("""
                1. Enter 1 to register
                2. Enter 2 to login """))

        if user_input == 1:
            self.register()
        elif user_input == 2:
            self.login()
        else:
            sys.exit(1000)