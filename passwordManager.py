# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sqlite3
import bcrypt
import getpass

class colors:
    white = '\033[97m\033[1m'
    green = '\033[92m\033[1m'
    blue = '\033[94m\033[1m'
    cyan = '\033[96m\033[1m'
    orange = '\033[93m\033[1m'
    red = '\033[91m\033[1m'
    end = '\033[0m'

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_manager (
    id_manager INTEGER PRIMARY KEY AUTOINCREMENT,
    service_manager TEXT VARCHAR(30),
    username_manager TEXT VARCHAR(30),
    password_manager TEXT VARCHAR(30)
);
''')

def menu():
    print('_____________________________')
    print('|   GERENCIADOR DE CONTAS   |')
    print('-----------------------------')
    print('| 1 - inserir novo registro |')
    print('| 2 - listar plataformas    |')
    print('| 3 - consultar login       |')
    print('| 4 - remover registro      |')
    print('| 5 - sair do programa      |')
    print('-----------------------------')

# 0 - FUNÇÃO PARA VALIDAR O LOGIN
def validate_login(usuario, senha):
    cursor.execute(f'''
        SELECT name_user FROM tb_user
        WHERE name_user = '{usuario}'
    ''')
    rows = cursor.fetchall()
    qnt_results = (len(rows))
    if qnt_results == 0:
        print(f'{colors.red}erro: usuario incorreto{colors.end}\n')
        exit()
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
        exit()

# 1 - INSERIR SERVIÇO/PLATAFORMA, NOME DE USUARIO E SENHA
def insert_password(service, username, password):
    cursor.execute(f'''
        INSERT INTO tb_manager (service_manager, username_manager, password_manager)
        VALUES('{service}', '{username}', '{password}')
    ''')
    print(f'{colors.green}sucesso: registro efetuado{colors.end}\n')
    conn.commit()

# 2 - CONSULTAR TODOS OS SERVIÇOS/PLATAFORMAS COM SEUS RESPECTIVOS IDs
def show_services():
    exist = 0
    cursor.execute('''
        SELECT id_manager, service_manager FROM tb_manager;
        ''')
    for result in cursor.fetchall():
        exist = int(len(result))
        print(f'{colors.white}id: {result[0]}\nplataforma: {result[1]}{colors.end}\n')
    if exist == 0:
        print(f'{colors.red}erro: nenhuma plataforma cadastrada{colors.end}')

# 3 - CONSULTAR NOME DE USUARIO E SENHA DE ACORDO COM O SERVIÇO
def get_password(service):
    cursor.execute(f'''
        SELECT username_manager, password_manager FROM tb_manager
        WHERE service_manager = '{service}'
    ''')
    rows = cursor.fetchall()
    # se qnt_results = 0, nao existe esse serviço na tabela
    qnt_results = (len(rows))
    if qnt_results == 0:  # cursor.rowcount == 0:
        print(f'{colors.red}erro: serviço não cadastrado{colors.end}')
    else:
        for resultado in rows:
            print(f'{colors.white}usuario/e-mail: {resultado[0]}\nsenha: {resultado[1]}{colors.end}\n')

# 4 - DELETAR UM DETERMINADO SERVIÇO/PLATAFORMA, PASSANDO O ID E O NOME SERVIÇO
def delete(id, service):
    cursor.execute(f'''
        DELETE FROM tb_manager
        WHERE id_manager = '{id}' and service_manager = '{service}' 
    ''')
    qnt_rowcount = cursor.rowcount
    if qnt_rowcount != 0:
        print(f'{colors.green}sucesso: registro removido{colors.end}\n')
    else:
        print(f'{colors.red}erro: id e serviço não identificado{colors.end}\n')
    conn.commit()

print('\nutilize o nome de usuario e a senha cadastrada no userManager-db.py\n')
usuario = input('insira o nome do usuario: ')
senha = getpass.getpass(prompt='insira sua senha: ', stream=None)
#senha = input('insira a senha: ')

validate_login(usuario, senha.encode('utf8'))

while True:
    # print('\n')
    menu()
    op = input('opção selecionada: ')
    print('\n')
    if op not in ['1', '2', '3', '4', '5']:
        print('erro: opção inválida')
        continue

    if op == '1':
        service = input('digite o nome da plataforma: ')
        username = input('digite o nome do usuario ou e-mail: ')
        password = input('digite a senha: ')
        insert_password(service, username, password)

    if op == '2':
        show_services()

    if op == '3':
        service = input('digite o nome da plataforma para obter o login: ')
        print('\n')
        get_password(service)

    if op == '4':
        id = input('digite o numero do id para excluir: ')
        service = input('digite o nome da plataforma para excluir: ')
        delete(id, service)

    if op == '5':
        print('programa finalizado')
        break

conn.close()
