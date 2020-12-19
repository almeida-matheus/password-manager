import string
import random
import argparse

LETTERS = string.ascii_letters
NUMBERS = string.digits
PUNCTUATION = string.punctuation
SPECIAL = '!@#$%&?'

def generate_password(letters=8, numbers=4, special=2):
    generated = ""
    generated += random_chars(letters, LETTERS)
    generated += random_chars(numbers, NUMBERS)
    generated += random_chars(special, SPECIAL)
    return shuffle_string(generated)

def shuffle_string(text): #funcao para embaralhar a string
    text = list(text) #transformar em lista ['a', 'b', 'c']
    random.shuffle(text) #embaralhr cada letra
    return ''.join(text) #transformar para uma string, tirando os ''

def random_chars(length, chars):
    generated = ""
    for x in range(length):
        generated += random.choice(chars) #choice = pegar 1 caractere aleatorio da lista
    return generated

if __name__ == '__main__': #se estiver rodando o programa nesse arquivo
    parser = argparse.ArgumentParser(description='Password Generetor')
    parser.add_argument('-l', type=int, default=8, help='letters quantity')
    parser.add_argument('-n', type=int, default=4, help='numbers quantity')
    parser.add_argument('-s', type=int, default=2, help='special characters quantity')
    args = parser.parse_args()
    print(generate_password(
        letters=args.l,
        numbers=args.n,
        special=args.s
    ))