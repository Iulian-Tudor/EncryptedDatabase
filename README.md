# EncrypteDatabase
Project in Python for my 3rd year of University

The task at hand requires me to make a tool capable of encrypting files and then storing them into a Database of my choice. It should also support reading files from the database, meaning decrypting them on demand, as well as deleting files from it altogether. To be noted I wasn't allowed to use specialized libraries such as the Cryptography library from Python, meaning the encryption and decryption is to be implemented manually. The project demands asymetric encryption, and I choose to go with RSA encryption, which is (probably) one of the most well known ones, following the guide written by IBM on RSA Asymetric Cryptography. The database chosen for easy managament is MongoDB, a no-SQL Database, that stores data in JSON format, which makes it ideal, as the tool doesn't require complex database schemas in order to be effective and organized.

**The Project is separated in modules:**

_1. Encryption module:_ Anything related to the cryptography involved part of the project can be found here, regarding asymetric RSA . Mandatory funtions being those to encrypt and decrypt the message/file.

_2. Hybrid module:_A rudimentary hybrid cryptography implementation, using a simple XOR for the symmetric part and the already existing RSA asymmetric functions for the asymmetric part. Mainly composed to be able to handle images and performance matters.

_3. Database module:_ Pretty self explanatory, it's the module where anything that has to interact with the Database goes into, whether we're talking about adding, removing or reading a file from the Database. It's, perhaps, the simplest and smallest module of them all, as once it's written, it, more or less, remains untouched.

_Future modules could be added, if I decide I want to incorporate 2 other projects into this one._
    
