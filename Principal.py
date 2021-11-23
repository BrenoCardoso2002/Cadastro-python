# Importações:
from datetime import datetime
from PyQt5.QtCore import Qt
import ctypes
import requests
from PyQt5 import QtWidgets, uic, QtGui
import pycep_correios
from pycep_correios import exceptions


# Função que verifica se há conexão com a internet:
def check_internet():
    # checar conexão de internet
    url = 'https://www.google.com'
    try:
        requests.get(url)
        return True
    except requests.exceptions.ConnectionError:
        return False


# Função validar Codigo
def ValidarCodigoCPF(Codigo):
    Codigo = Codigo.replace(".", "")
    Codigo = Codigo.replace("-", "")
    if Codigo[0] == Codigo[1] == Codigo[2] == Codigo[3] == Codigo[4] == Codigo[5] == Codigo[6] == Codigo[7] == Codigo[8] == Codigo[9] == Codigo[10]:
        return False
    else:
        # calcula o primeiro digito:
        i = 10
        soma1 = 0
        for j in range(9):
            soma1 += (int(Codigo[j]) * i)
            i -= 1
        d1 = (soma1 * 10) % 11
        if d1 != int(Codigo[9]):
            return False
        else:
            m = 11
            soma2 = 0
            for n in range(10):
                soma2 += (int(Codigo[n]) * m)
                m -= 1
            d2 = (soma2 * 10) % 11
            if d2 != int(Codigo[10]):
                return False
            else:
                return True


# Função que válida a data de nascimento:
def ValidarData(Data):
    AnoNasc = Data[-4::]
    AnoAtual = datetime.today().strftime('%Y')
    Diferenca = int(AnoAtual) - int(AnoNasc)
    if Diferenca > 0:
        return True
    else:
        return False


# classe principal:
class Principal:
    def __init__(self):
        # Variaveis para incialição e manipulação da tela e de seus componentes:
        app = QtWidgets.QApplication([])
        self.tela = uic.loadUi("interface.ui")

        # define algumas propriedades da self.tela
        self.tela.setFixedSize(720, 295)
        self.tela.setWindowIcon(QtGui.QIcon('Logo.png'))

        # define algumas propriedades na caixa de texto do CPF:
        self.tela.Txt_CPF.setInputMask("999.999.999-99")
        self.tela.Txt_CPF.textChanged.connect(self.CPFChanged)

        # define algumas propriedades na caixa de texto do CEP:
        self.tela.Txt_CEP.setInputMask("99999-999")
        self.tela.Txt_CEP.textChanged.connect(self.CEPChanged)

        # define algumas propriedades na caixa de texto do telefone celular:
        self.tela.Txt_Celular.setInputMask("(99) 99999-9999")

        # define algumas propriedades na caixa de texto do telefone celular:
        self.tela.Txt_Fixo.setInputMask("(99) 9999-9999")

        # define algumas propriedades no botão que exibe o endereço completo:
        self.tela.Bt_TodoEndereco.setCursor(Qt.PointingHandCursor)
        self.tela.Bt_TodoEndereco.clicked.connect(self.ShowTodoEndereco)

        # define algumas propriedades no botão de realizar cadastro:
        self.tela.Bt_Cadastrar.setCursor(Qt.PointingHandCursor)
        self.tela.Bt_Cadastrar.clicked.connect(self.CadastrarUsuario)

        # desabilita os campos que mostram o endereço do usuário:
        self.tela.Txt_Logradouro.setEnabled(False)
        self.tela.Txt_Bairro.setEnabled(False)
        self.tela.Txt_Cidade.setEnabled(False)
        self.tela.Txt_UF.setEnabled(False)

        # comando que inicializa a self.tela e comando que permite que a self.tela fique aberta até que o usuário a feche:
        self.tela.show()
        app.exec()

    # Função que capta a mudança de texto no campo do cep:
    def CEPChanged(self):
        cep = self.tela.Txt_CEP.text()
        if len(cep) == 9:
            self.PesquisaCEP(cep)
        else:
            self.tela.Txt_Logradouro.setText("")
            self.tela.Txt_Bairro.setText("")
            self.tela.Txt_Cidade.setText("")
            self.tela.Txt_UF.setText("")

    # Função que realiza a pesquisa do cep:
    def PesquisaCEP(self, cep):
        try:
            endereco = pycep_correios.get_address_from_cep(cep)
            self.tela.Txt_Logradouro.setText(endereco['logradouro'])
            self.tela.Txt_Bairro.setText(endereco['bairro'])
            self.tela.Txt_Cidade.setText(endereco['cidade'])
            self.tela.Txt_UF.setText(endereco['uf'])
        except exceptions.InvalidCEP:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")
        except exceptions.CEPNotFound:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")
        except exceptions.ConnectionError:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")
        except exceptions.Timeout:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")
        except exceptions.HTTPError:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")
        except exceptions.BaseException:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")

    # Função que mostra o endereço completo:
    def ShowTodoEndereco(self):
        try:
            cep = self.tela.Txt_CEP.text()
            if len(cep) != 9:
                ctypes.windll.user32.MessageBoxW(0, "CEP incompelto!!!", "Erro!!", 16)
                self.tela.Txt_CEP.setText("")
            else:
                endereco = pycep_correios.get_address_from_cep(cep)
                Texto = "{}\n{}\n{}\n{}\n".format(endereco['logradouro'],
                                                  endereco['bairro'],
                                                  endereco['cidade'],
                                                  endereco['uf'])
                ctypes.windll.user32.MessageBoxW(0, Texto, "Todo o Endereço!", 1)
        except exceptions.InvalidCEP:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")
        except exceptions.CEPNotFound:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")
        except exceptions.ConnectionError:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")
        except exceptions.Timeout:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")
        except exceptions.HTTPError:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")
        except exceptions.BaseException:
            ctypes.windll.user32.MessageBoxW(0, "CEP Inválido!", "Erro!!", 16)
            self.tela.Txt_CEP.setText("")

    # Função de mudança de texto no campo CPF:
    def CPFChanged(self):
        cpf = self.tela.Txt_CPF.text()
        if len(cpf) == 14:
            if not ValidarCodigoCPF(cpf):
                ctypes.windll.user32.MessageBoxW(0, "CPF Inválido!", "Erro!!", 16)
                self.tela.Txt_CPF.setText("")

    # Função de clique do botão cadastrar:
    def CadastrarUsuario(self):
        # Obtem uma variável para cada campo:txt_Nome
        Usuario = self.tela.Txt_Nome.text().lower()
        CPF = self.tela.Txt_CPF.text()
        Email = self.tela.Txt_Email.text().lower()
        Nascimento = self.tela.Dt_Nascimento.text()
        CEP = self.tela.Txt_CEP.text()
        Numero = self.tela.Txt_Numero.text()
        Complemento = self.tela.Txt_Complemento.text().lower()
        Celular = self.tela.Txt_Celular.text()
        Fixo = self.tela.Txt_Fixo.text()

        # verifica se há algum campo em branco:
        if Usuario.replace(" ", "") == "" or CPF.replace(" ", "") == "" or Email.replace(" ", "") == "" or CEP.replace(" ", "") == "" or Numero.replace(" ", "") == "" or Complemento.replace(" ", "") == "" or Celular.replace(" ", "") == "" or Fixo.replace(" ", "") == "":
            ctypes.windll.user32.MessageBoxW(0, "Há algum campo em branco", "Erro!!", 16)
        else:
            if len(CPF.replace(" ", "")) != 14:
                ctypes.windll.user32.MessageBoxW(0, "CPF inválido", "Erro!!", 16)
            else:
                if len(CEP.replace(" ", "") != 9):
                    ctypes.windll.user32.MessageBoxW(0, "CEP inválido", "Erro!!", 16)
                else:
                    if len(Celular.replace(" ", "")) != 14 or len(Fixo.replace(" ", "")) != 13:
                        ctypes.windll.user32.MessageBoxW(0, "Telefones inválido", "Erro!!", 16)
                    else:
                        if not ValidarData(Nascimento):
                            ctypes.windll.user32.MessageBoxW(0, "Data inválida", "Erro!!", 16)
                        else:
                            ctypes.windll.user32.MessageBoxW(0, "Data válido", "Sucesso!!", 1)


# Condicional que verifica se há a conexão:
if check_internet():
    # Chama a função principal do programa:
    Principal = Principal()
else:
    ctypes.windll.user32.MessageBoxW(0, "Não há conexão com a internet!!!", "Erro!!", 16)
