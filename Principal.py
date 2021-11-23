# Importações:
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

        # define algumas propriedades na caixa de texto do CEP:
        self.tela.Txt_CEP.setInputMask("99999-999")
        self.tela.Txt_CEP.textChanged.connect(self.CEPChanged)

        # define algumas propriedades na caixa de texto do telefone celular:
        self.tela.Txt_Celular.setInputMask("(99) 99999-9999")

        # define algumas propriedades na caixa de texto do telefone celular:
        self.tela.Txt_Fixo.setInputMask("(99) 9999-9999")

        # define algumas propriedades no botão que exibe o endereço completo:
        self.tela.Bt_TodoEndereco.setCursor(Qt.PointingHandCursor)

        # define algumas propriedades no botão de realizar cadastro:
        self.tela.Bt_Cadastrar.setCursor(Qt.PointingHandCursor)

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


# Condicional que verifica se há a conexão:
if check_internet():
    # Chama a função principal do programa:
    Principal = Principal()
else:
    ctypes.windll.user32.MessageBoxW(0, "Não há conexão com a internet!!!", "Erro!!", 16)
