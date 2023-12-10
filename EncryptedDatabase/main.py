import sys

from database.database import Database
from encryption.encryption import Encryption
from hybrid.hybrid import HybridEncryption


def main():
    """
    Main function to run the application.

    This function initializes the database and encryption keys, 
    then enters a loop to present a menu to the user. The user can 
    choose to add a file to the database, retrieve a file, delete a 
    file, delete all files, view the database, or exit the program.
    """
    database = Database()
    p = 599
    q = 101
    public_key, private_key = Encryption.generate_key_pair(p, q)

    menu = {
        1: lambda: database.add_file_to_database(input("\nEnter file path: "), public_key,
                                                 HybridEncryption.generate_symmetric_key(),
                                                 input("\nEnter encryption method (RSA/Hybrid): ")),
        2: lambda: database.get_file_from_database(input("\nEnter file name: "), private_key),
        3: lambda: database.delete_file(input("\nEnter file name: ")),
        4: lambda: database.delete_all_files(),
        5: lambda: database.view_database(),
        6: lambda: sys.exit(),
    }


    while True:
        print("\nEncryptedDatabase MENU:")
        print("1. Add file to database")
        print("2. Get file from database")
        print("3. Delete file from database")
        print("4. Delete all")
        print("5. View database")
        print("6. Exit")

        choice = int(input("Enter your choice: "))

        if choice in menu:
            menu[choice]()
        else:
            print("Invalid choice")


if __name__ == '__main__':
    main()
