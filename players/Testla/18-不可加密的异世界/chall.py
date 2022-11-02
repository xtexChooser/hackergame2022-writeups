# challenge source code
# Env: Python 3.10

import os
import typing
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad
from magic_box import *

banner = """
Traveler, choose one God to talk with.
1. Negligent God
2. Softhearted God
3. Harsh God
Other. exit()
"""

weak_keys = [
    bytes.fromhex('0101010101010101'),
    bytes.fromhex('FEFEFEFEFEFEFEFE'),
    bytes.fromhex('E0E0E0E0F1F1F1F1'),
    bytes.fromhex('1F1F1F1F0E0E0E0E'),
]

# for weak_key in weak_keys:
#     box = Magic_box('DES', 'ECB', weak_key)
#     plaintext = secrets.token_bytes(8)
#     assert box.auto_enc(box.auto_enc(plaintext)) == plaintext


def aes_ecb_decrypt(key: bytes, cipher_text: bytes) -> bytes:
    box = Magic_box('AES', 'ECB', key)
    return box.auto_dec(cipher_text)


# p = bytes.fromhex(input('Pass from god:'))
block_num = 10
key = b'\x00' * 16
data = b'\x00' * 16
for i in range(block_num):
    data = aes_ecb_decrypt(key, data)
    print((key + data).hex())
    # print(p[i*16:(i+1)*16])
    # box = Magic_box('AES', 'OFB', key + iv)
    # print(box.auto_enc(p)[i*16:(i+1)*16])
# exit()

solved_data = bytes.fromhex('87ab9068aee7aba2dce8dbe475244e47')
print(long_to_bytes(crc128(solved_data), 16).hex())
exit()


def Negligent_God():
    print("Who are u?")
    your_name = input("> name: ")
    your_pass = your_name + "Open the door!"

    print("Uh, I don't care who you are. Just show me your magic power.")
    algo = input("> algo: ")
    mode = input("> mode: ")

    assert algo in algos
    assert mode in modes

    if algo == "AES":
        blocksize = 16
    else:
        blocksize = 8

    keys = bytes.fromhex(input("> hex keys: "))
    magic_box = Magic_box(algo, mode, keys)

    if magic_box.auto_enc(pad(your_pass.encode(), blocksize)) == pad(your_pass.encode(), blocksize):
        print("Well done")
        print(open("./flag1", "r").read())
    else:
        print("I'm sorry, maybe something is wrong with your name? Um, I just say it casually.")


def Softhearted_God():
    print("Who are u?")
    your_name = input("> name: ")

    print("Oh, what a poor guy from another world. You are allowed to show me your magic power block by block.")
    algo = input("> algo: ")
    mode = input("> mode: ")

    assert algo in algos
    assert mode in modes

    block_num = 10

    if algo == "AES":
        blocksize = 16
    else:
        blocksize = 8

    your_pass = os.urandom(block_num*blocksize)
    print(f"[+] you_pass : {your_pass.hex()}")

    for i in range(block_num):
        print(f"[+] rounds {i}")

        keys = bytes.fromhex(input("> hex keys: "))
        magic_box = Magic_box(algo, mode, keys)

        if magic_box.auto_enc(your_pass)[i*blocksize:(i+1)*blocksize] != your_pass[i*blocksize:(i+1)*blocksize]:
            print("You're not a pure guy from another world!")
            return

    print("Well done")
    print(open("./flag2", "r").read())


def Harsh_God():
    print("Treat no exceptions. You're not allowed to select the keys directly.")
    print("Anyway, this time I want to encrypt the message twice.")

    your_name = input("> name: ")
    algo = input("> algo: ")
    mode = input("> mode: ")

    assert algo in algos
    assert mode in modes

    if algo == "AES":
        blocksize = 16
    else:
        blocksize = 8

    your_pass = bytes.fromhex(input("> hex msg (at least 16 bytes): "))

    assert len(your_pass) >= 16 and len(your_pass) % blocksize == 0, "Invalid msg length"

    your_key = long_to_bytes(crc128(your_pass), 16)[:blocksize]

    if mode != "ECB":
        iv = os.urandom(blocksize)
        magic_box = Magic_box(algo, mode, your_key+iv)
    else:
        magic_box = Magic_box(algo, mode, your_key)

    if magic_box.auto_enc(magic_box.auto_enc(your_pass)) == your_pass:
        print("What a miracle!")
        print(open("./flag3", "r").read())
    else:
        print("Out, Right Now!")


if __name__ == "__main__":
    while True:
        print(banner)

        try:
            choice = int(input("> choice: "))
        except:
            print("Must be a digit number")
            continue

        if choice == 1:
            Negligent_God()
        elif choice == 2:
            Softhearted_God()
        elif choice == 3:
            Harsh_God()
        else:
            print("Byebye!")
            exit()
