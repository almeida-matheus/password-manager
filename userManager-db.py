# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sqlite3
import bcrypt
import re
import getpass

class colors:
    white = '\033[97m\033[1m'
    green = '\033[92m\033[1m'
    blue = '\033[94m\033[1m'
    cyan = '\033[96m\033[1m'
    orange = '\033[93m\033[1m'
    red = '\033[91m\033[1m'
    end = '\033[0m'

banco = sqlite3.connect('database.db')
cursor = banco.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_user (
    name_user TEXT VARCHAR(30) PRIMARY KEY,
    password_user TEXT VARCHAR(30)
);
''')

def menu():
    print('_____________________________')
    print('|  GERENCIADOR DE USUARIOS  |')
    print('-----------------------------')
    print('| 1 - inserir novo usuario  |')
    print('| 2 - listar todos usuarios |')
    print('| 3 - validar usuario       |')
    print('| 4 - remover usuario       |')
    print('| 5 - sair do programa      |')
    print('-----------------------------')

# 1 - FUNÇÃO PARA VALIDAR A SENHA DO USUARIO
def validate_password(usuario, senha):
    maiuscula = re.search(r'[A-Z]', senha)
    numero = re.search(r'[0-9]', senha)
    especial = re.search(r'[!@#$%<^&*?]', senha)
    if len(senha) < 8 or len(senha) > 50:
        print(f'{colors.orange}senha fraca: digite pelo menos 8 caracteres{colors.end} \n')
        return 1
    elif numero == None:
        print(f'{colors.orange}senha fraca: digite pelo menos 1 numero{colors.end} \n')
        return 1
    elif maiuscula == None:
        print(f'{colors.orange}senha fraca: digite pelo menos 1 caractere maiusculo{colors.end} \n')
        return 1
    elif especial == None:
        print(f'{colors.orange}senha media: digite pelo menos 1 caractere especial{colors.end} \n')
        return 1
    else:
        # strip: remover espaços / upper: colocar caractere em maiusculo / [0]: levar o 1 caractere em consideração
        confirmar = str(
            input('confirmar: [digite SIM ou NÃO]: ')).strip().upper()[0]
        if confirmar not in 'SsYy':
            return 0
        else:
            check_name_exists(usuario, senha)

# 1 - FUNÇÃO PARA CHECAR SE O USUARIO JA EXISTE
def check_name_exists(usuario, senha):
    cursor.execute(f'''
                SELECT name_user FROM tb_user
                WHERE name_user = '{usuario}'
            ''')
    rows = cursor.fetchall()
    qnt_results = (len(rows))
    # se tiver esse usuario com esse nome len(row) = [1], se nao row = []
    if qnt_results == 0:
        print(f'{colors.green}sucesso: usuario adicionado{colors.end}\n')
        encrypt_password(usuario, senha)
        return 0
    else:
        print(f'{colors.red}erro: esse usuario já existe{colors.end}\n')
        return 0


# 1 - FUNÇÃO PARA CRIPTOGRAFAR A SENHA E ADICIONAR NA TABELA
def encrypt_password(usuario, senha):
    hash_password = bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt())
    cursor.execute('INSERT INTO tb_user (name_user, password_user) VALUES ("%s", "%s")' % (
        usuario, hash_password))
    banco.commit()


# 2 - FUNÇÃO PARA LISTAR TODOS OS USUARIOS
def show_name():
    i = 0
    exist = 0
    cursor.execute('''
        SELECT name_user FROM tb_user;
    ''')
    for name in cursor.fetchall():
        i = i + 1
        exist = int(len(name[0]))
        print(f'{colors.white}usuario {i}: {name[0]}{colors.end}\n')
    if exist == 0:
        print(f'{colors.red}erro: não há usuarios{colors.end}\n')

# 3 - FUNÇÃO PARA VALIDAR O LOGIN
def validate_login(usuario, senha):
    cursor.execute(f'''
        SELECT name_user FROM tb_user
        WHERE name_user = '{usuario}'
    ''')
    rows = cursor.fetchall()
    qnt_results = (len(rows))
    if qnt_results == 0:
        print(f'{colors.red}erro: usuario incorreto{colors.end}\n')
    else:
        cursor.execute(f'''
            SELECT password_user FROM tb_user
            WHERE name_user = '{usuario}';
        ''')
    # [("b'$2bTkVkOe'",)]
    hash_password = cursor.fetchall()
    # ("b'$2bTkVkOe'",)
    hash_password = str(hash_password[0])
    # $2bTkVkOe
    hash_password = hash_password[4:int(len(hash_password) - 4)]
    # b'$2bTkVkOe'
    hash_password = hash_password.encode('utf8')
    # se a senha condiz com o hash da tabela = True
    if bcrypt.checkpw(senha, hash_password):
        print(f'{colors.green}sucesso: o usuario coresponde a senha{colors.end}\n')
    else:
        print(f'{colors.red}erro: senha incorreta{colors.end}\n')

# 4 - FUNÇÃO PARA REMOVER USUARIO
def remove_user(usuario):
    cursor.execute(f'''
            DELETE FROM tb_user
            WHERE name_user = '{usuario}'
        ''')
    qnt_rowcount = cursor.rowcount
    if qnt_rowcount != 0:
        print(f'{colors.green}sucesso: usuario {usuario} removido{colors.end}\n')
    else:
        print(f'{colors.red}erro: usuario não identificado{colors.end}\n')
    banco.commit()

while True:
    menu()
    op = input('opção selecionada: ')
    print('\n')
    if op not in ['1', '2', '3', '4', '5']:
        print('erro: opção inválida')
        continue

    if op == '1':
        repeat = ()
        while repeat != 0:
            usuario = input('insira o novo nome do usuario: ')
            senha = getpass.getpass(prompt='insira sua senha: ', stream=None)
            #senha = input('insira a nova senha: ')
            repeat = validate_password(usuario, senha)

    if op == '2':
        show_name()

    if op == '3':
        usuario = input('insira o nome do usuario: ')
        senha = getpass.getpass(prompt='insira sua senha: ', stream=None)
        #senha = input('insira a senha: ')
        validate_login(usuario, senha.encode('utf8'))

    if op == '4':
        usuario = input('digite o nome do usuario para remover: ')
        remove_user(usuario)

    if op == '5':
        print('programa finalizado')
        break

banco.close()
