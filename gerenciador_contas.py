import sqlite3
import bcrypt
import getpass

conn = sqlite3.connect('banco_de_dados.db') #windows:('C:\\python\\arquivo.db') linux:('/root/arquivo.db')
cursor = conn.cursor()

#TABELA DE REGISTROS DO PROGRAMA
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    idt integer PRIMARY KEY AUTOINCREMENT,
    service text,
    username text,
    password text
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

#CONSULTAR NOME DE USUARIO E SENHA DE ACORDO COM O SERVIÇO - 3
def get_password(service):
    cursor.execute(f'''
        SELECT username, password FROM users
        WHERE service = '{service}'
    ''')
    rows = cursor.fetchall()
    qnt_results = (len(rows)) #se qnt_results = 0, nao existe esse serviço na tabela
    if qnt_results == 0: #cursor.rowcount == 0:
        print('erro: serviço não cadastrado')
    else:
        for resultado in rows:
            print(f'usuario/e-mail: {resultado[0]} senha: {resultado[1]}')

#INSERIR SERVIÇO/PLATAFORMA, NOME DE USUARIO E SENHA - 1
def insert_password(service, username, password):
    cursor.execute(f'''
        INSERT INTO users (service, username, password)
        VALUES('{service}', '{username}', '{password}')
    ''')
    print('sucesso: registro efetuado')
    conn.commit()

#CONSULTAR TODOS OS SERVIÇOS/PLATAFORMAS COM SEUS RESPECTIVOS IDs - 2
def show_services():
    cursor.execute('''
        SELECT idt, service FROM users;
        ''')
    for result in cursor.fetchall():
        print(f'ID: {result[0]} plataforma: {result[1]}')

#DELETAR UM DETERMINADO SERVIÇO/PLATAFORMA, PASSANDO O ID E O NOME SERVIÇO - 4
def delete(idt,service):
    cursor.execute(f'''
        DELETE FROM users
        WHERE idt = '{idt}' and service = '{service}' 
    ''')
    qnt_rowcount = cursor.rowcount
    if qnt_rowcount != 0:
        print('sucesso: registro removido')
    else:
        print('erro: id e serviço não identificado')
    conn.commit()

#VALIDAR SE O USUARIO E A SENHA FOI DIGITADA CORRETAMENTE - 0
def validar_login(usuario,senha):
    cursor.execute(f'''
        SELECT usuario FROM USUARIOS
        WHERE usuario = '{usuario}'
    ''')
    rows = cursor.fetchall()
    qnt_results = (len(rows)) #qnt_resulta = 0, não existe esse usuario na tabela
    if qnt_results == 0:
        print('erro: usuario incorreto')
        exit()
    else:
        cursor.execute(f'''
            SELECT hash_senha FROM USUARIOS WHERE usuario = '{usuario}';
        ''')
        for hash_senha in cursor.fetchall():
            hash_senha = str(hash_senha)
            hash_senha = hash_senha[4:int(len(hash_senha) - 4)]
            hash_senha = hash_senha.strip()
            hash_senha = hash_senha.encode('utf8')
            if bcrypt.checkpw(senha, hash_senha):  # se a senha condiz com o hash da tabela = True
                print('sucesso: login efetuado')
            else:
                print('erro: senha incorreta')
                exit()

print('\nutilize o nome de usuario e a senha cadastrada no programa: gerenciador_usuarios\n')
usuario = input('insira o nome do usuario: ')
senha = getpass.getpass(prompt='insira sua senha: ', stream=None)
#senha = input('insira a senha: ')

validar_login(usuario,senha.encode('utf8'))

while True:
    print('\n')
    menu()
    op = input('opção selecionada: ')
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
        service = input('digite o nome da plataforma para obter o login:  ')
        get_password(service)

    if op == '4':
        idt = input('digite o numero do id para excluir: ')
        service = input('digite o nome da plataforma para excluir: ')
        delete(idt,service)

    if op == '5':
        print('programa finalizado')
        break

conn.close()