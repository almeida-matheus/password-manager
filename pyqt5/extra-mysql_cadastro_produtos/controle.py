from PyQt5 import  uic,QtWidgets
import pymysql
from reportlab.pdfgen import canvas

banco = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)
'''
DIGITAR NO CMD DO MYSQL
create database cadastro_produtos
'''
cursor = banco.cursor()

cursor.execute ("CREATE TABLE IF NOT EXISTS produtos(id INT NOT NULL AUTO_INCREMENT, codigo INT, descricao VARCHAR(50), valor DOUBLE, categoria VARCHAR(20), PRIMARY KEY (id))")


def funcao_principal():
    linha1 = formulario.lineEdit.text() #le oq foi digitado nessa linha do formulario
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()

    categoria = ""
    
    if formulario.radioButton.isChecked() :
        print("Categoria Roupa selecionada")
        categoria ="Roupa"
    elif formulario.radioButton_2.isChecked() :
        print("Categoria Eletronicos selecionada")
        categoria ="Eletronico"
    else :
        print("Categoria Alimentos selecionada")
        categoria ="Alimento"

    print("Codigo:",linha1)
    print("Descricao:",linha2)
    print("Valor:",linha3)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,valor,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()
    formulario.lineEdit.setText("") #limpar os campos apos clicar no enviar
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")

def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall() #vai pegar oq foi feito na ultima linha do cursor e vai salvar nessa variavel
    print(dados_lidos[0][0]) #pegar um elemento especifico passando linha e coluna
    #gerar a tabela
    segunda_tela.tableWidget.setRowCount(len(dados_lidos)) #quantas linhas vai ter essa tabela
    segunda_tela.tableWidget.setColumnCount(5) #definir o numero de colunas
    #salvar no banco de dados
    for i in range(0, len(dados_lidos)): #varre linhas
        for j in range(0,5): #varre colunas
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall() #vai pegar oq foi feito na ultima linha do cursor e vai salvar nessa variavel
    print(dados_lidos)
    y = 0
    pdf = canvas.Canvas("cadastro_produto.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Produtos cadastrados") # x e y, e de baixo para cima, 800 e em cima, na primeira linha
    
    pdf.setFont("Times-Bold", 18)
    #escrever na msm linha
    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "CODIGO")
    pdf.drawString(210,750, "PRODUTO")
    pdf.drawString(310,750, "VALOR")
    pdf.drawString(410,750, "CATEGORIA")

    for i in range(0, len(dados_lidos)): #for ate o tamanho dos dados obtidos
        y = y + 50 #pra diminuir o valor do y e ir pulando uma linha ate fica mais em baixo
        pdf.drawString(10,750 - y, str(dados_lidos[i][0])) #depois passa o valor obtido
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))
    
    pdf.save()
    print("PDF gerado com sucesso")






app=QtWidgets.QApplication([]) #b - criar aplicacao
formulario=uic.loadUi("formulario.ui") #b - importa o arquivo gerado pelo qt designer
segunda_tela=uic.loadUi("listar_dados.ui")
formulario.pushButton.clicked.connect(funcao_principal) #b - utilizando o nome do botao da ui, ao clicar executa a funcao principal
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(gerar_pdf)


formulario.show() #aparecer a tela
app.exec()


# criando a tabela

""" create table produtos (id INT NOT NULL AUTO_INCREMENT,
codigo INT,
descricao VARCHAR(50),  
preco DOUBLE,
categoria VARCHAR(20),
PRIMARY KEY (id)
);  """

# inserindo registros na tabela

#INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (123,"impressora",500.00,"informatica"); 
