from PyQt5 import  uic,QtWidgets
import sqlite3


def chama_tela_principal():
    tela_login.label_4.setText("") #limpar o texto login incorreto quando abrir
    nome_usuario = tela_login.lineEdit.text()
    senha = tela_login.lineEdit_2.text()
    if nome_usuario == "teste" and senha == "teste123" :
        tela_login.close()
        tela_principal.show()
    else :
        tela_login.label_4.setText("erro: dados de login incorretos")
    

def logout():
    tela_principal.close()
    tela_login.show()

def abre_tela_cadastro():
    tela_cadastro.show()


def cadastrar():
    nome = tela_cadastro.lineEdit.text()
    login = tela_cadastro.lineEdit_2.text()
    senha = tela_cadastro.lineEdit_3.text()
    c_senha = tela_cadastro.lineEdit_4.text()

    if (senha == c_senha):
        try:
            banco = sqlite3.connect('banco_cadastro.db') 
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome text,login text,senha text)")
            cursor.execute("INSERT INTO cadastro VALUES ('"+nome+"','"+login+"','"+senha+"')")

            banco.commit() 
            banco.close()
            tela_cadastro.label.setText("sucesso: usuario cadastrado")

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ",erro)
    else:
        tela_cadastro.label.setText("erro: as senhas digitadas estão diferentes")
    

    


app=QtWidgets.QApplication([])
tela_login=uic.loadUi("tela_login.ui")
tela_principal = uic.loadUi("tela_principal.ui")
tela_cadastro = uic.loadUi("tela_cadastro.ui")
tela_login.pushButton.clicked.connect(chama_tela_principal)
tela_principal.pushButton.clicked.connect(logout)
tela_login.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password) #para nao aparecer a senha ao digitar
tela_login.pushButton_2.clicked.connect(abre_tela_cadastro)
tela_cadastro.pushButton.clicked.connect(cadastrar) 


tela_login.show()
app.exec()