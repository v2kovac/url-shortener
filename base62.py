alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
base = len(alphabet)

def encode(number):
    string = ''
    while(number > 0):
        string = alphabet[number % base] + string
        number //= base
    return string

def decode(string):
    number = 0
    for char in string:
        number = number * base + alphabet.index(char)
    return number
