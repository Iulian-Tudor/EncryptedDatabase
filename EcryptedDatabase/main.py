import sys
sys.path.insert(0, 'EcryptedDatabase/database')
sys.path.insert(0, 'EcryptedDatabase/encryption')

from database import add_file_to_database, get_file_from_database, delete_file, view_database
from encryption import key_generator
def main():

    public_key, private_key = key_generator(3, 11)

    menu = {
        1: lambda: add_file_to_database(input("\nEnter file path: "), public_key),
        2: lambda: get_file_from_database(input("\nEnter file path: "), private_key),
        3: lambda: delete_file(input("\n1Enter file path: ")),
        4: view_database,
        5: lambda: sys.exit(),
    }

    while True:
        print("\nMENU:")
        print("1. Add file to database")
        print("2. Get file from database")
        print("3. Delete file from database")
        print("4. View database")
        print("5. Exit")

        choice = int(input("Enter your choice: "))
        
        if choice in menu:
            menu[choice]()
        else:
            print("Invalid choice")


if __name__ == '__main__':
    main()