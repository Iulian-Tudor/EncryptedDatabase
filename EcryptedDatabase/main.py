import sys
sys.path.insert(0, 'EncryptedDatabase/database')
sys.path.insert(0, 'EncryptedDatabase/encryption')

from database.database import Database
from encryption.encryption import Encryption

def main():

    database = Database()
    p=599
    q=101
    public_key, private_key = Encryption.generate_key_pair(p,q)

    menu = {
        1: lambda: database.add_file_to_database(database, input("\nEnter file path: "), public_key),
        2: lambda: database.get_file_from_database(database, input("\nEnter file name: "), private_key),
        3: lambda: database.delete_file(database, input("\nEnter file name: ")),
        4: lambda: database.view_database(database),
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
