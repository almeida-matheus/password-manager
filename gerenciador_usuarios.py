import sqlite3
import bcrypt
import re
import getpass

banco = sqlite3.connect('banco_de_dados.db') #windows:('C:\\python\\arquivo.db') linux:('/root/arquivo.db')
cursor = banco.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS USUARIOS (
    usuario text PRIMARY KEY,
    hash_senha text
);
''')
banco.commit()

#FUNÇÃO PARA VALIDAR A SENHA DO USUARIO - 1
def validar_digito(usuario,senha):
    maiuscula = re.search(r'[A-Z]', senha)
    numero = re.search(r'[0-9]',senha)
    especial = re.search(r'[!@#$%<^&*?]', senha)
    if len(senha) < 8 or len(senha) > 100:
        print('senha fraca: digite pelo menos 8 caracteres\n')
        return 1
    elif numero == None:
        print('senha fraca: digite pelo menos 1 numero\n')
        return 1
    elif maiuscula == None:
        print('senha fraca: digite pelo menos 1 caractere maiusculo\n')
        return 1
    elif especial == None:
        print('senha media: digite pelo menos 1 caractere especial\n')
        return 1
    else:
        confirmar = str(input('confirmar: [digite SIM ou NÃO]: ')).strip().upper()[0]
        if confirmar not in 'SsYy':
            return 0
        else:
            usuario_repetido(usuario,senha)
            return 0

#FUNÇÃO PARA CHECAR SE O USUARIO JA EXISTE - 1
def usuario_repetido(usuario,senha):
    cursor.execute(f'''
                SELECT hash_senha FROM USUARIOS
                WHERE usuario = '{usuario}'
            ''')
    rows = cursor.fetchall()
    qnt_results = (len(rows))
    #se tiver esse usuario row = [hash_senha], se nao row = []
    if qnt_results == 0:
        print('sucesso: usuario adicionado')
        insere_encriptado(usuario, senha)
        return 0
    else:
        print('erro: esse usuario já existe')
        return 0


#FUNÇÃO PARA CRIPTOGRAFAR A SENHA E ADICIONAR NA TABELA - 1
def insere_encriptado(usuario,senha):
    hash_senha = bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt())
    cursor.execute('insert into USUARIOS values ("%s", "%s")' % (usuario, hash_senha))
    banco.commit()

#FUNÇÃO PARA VALIDAR O LOGIN - 3
def validar_login(usuario,senha):
    cursor.execute(f'''
        SELECT usuario FROM USUARIOS
        WHERE usuario = '{usuario}'
    ''')
    rows = cursor.fetchall()
    qnt_results = (len(rows)) #se qnt_resulta = 0, nao existe esse usuario na tabela
    if qnt_results == 0:  # cursor.rowcount == 0:
        print('erro: usuario incorreto\n')
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
                print('sucesso: o usuario coresponde a senha')
            else:
                print('erro: senha incorreta\n')

#FUNÇÃO PARA LISTAR TODOS OS USUARIOS - 2
def listar_usuario():
    i = 0
    exist = 0
    cursor.execute('''
            SELECT usuario FROM USUARIOS;
            ''')
    for usuario in cursor.fetchall():
        i = i + 1
        exist = int(len(usuario[0]))
        print(f'usuario {i}: {usuario[0]}')
    if exist == 0:
        print('erro: não há usuarios')


#FUNÇÃO PARA REMOVER USUARIO - 4
def remover_usuario(usuario):
    cursor.execute(f'''
            DELETE FROM USUARIOS
            WHERE usuario = '{usuario}'
        ''')
    qnt_rowcount = cursor.rowcount
    if qnt_rowcount != 0:
        print('sucesso: usuario removido')
    else:
        print('erro: usuario não identificado')
    banco.commit()

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

while True:
    print('\n')
    menu()
    op = input('opção selecionada: ')
    if op not in ['1', '2', '3', '4', '5']:
        print('erro: opção inválida')
        continue

    if op == '1':
        cont = ()
        while cont != 0:
            usuario = input('insira o novo nome do usuario: ')
            senha = getpass.getpass(prompt='insira sua senha:', stream=None)
            #senha = input('insira a nova senha: ')

            cont = validar_digito(usuario, senha)

    if op == '2':
        listar_usuario()

    if op == '3':
        usuario = input('insira o nome do usuario: ')
        senha = getpass.getpass(prompt='insira sua senha:', stream=None)
        #senha = input('insira a senha: ')

        validar_login(usuario, senha.encode('utf8'))

    if op == '4':
        usuario = input('digite o nome do usuario para remover: ')
        remover_usuario(usuario)

    if op == '5':
        print('programa finalizado')
        break

banco.close()