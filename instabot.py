from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from time import sleep
import sqlite3
import base64
import random

from win32comext.axscript.server.error import Exception

from database import *

class instabot:
    # O local de execução do nosso script
    dir_path = os.getcwd()

    # O caminho do chromedriver
    chromedriver = os.path.join(dir_path, "chromedriver.exe")

    # função pra login
    def login(self, username, password):

        print(f'[+] logando na conta @{username}')

        self.driver.get('https://www.instagram.com/')  # instagram url
        sleep(2)

        userelement = self.driver.find_element_by_xpath('//input[@name="username"]')
        userelement.clear()
        userelement.send_keys(username)

        pwdelement = self.driver.find_element_by_xpath('//input[@name="password"]')
        pwdelement.clear()
        pwdelement.send_keys(password)
        pwdelement.send_keys(Keys.RETURN)
        sleep(5)

    # comentar em publicação
    def comment(self, url, comment, cont, username):
        self.driver.get(url)
        sleep(2)
        self.driver.find_element_by_class_name('Ypffh').click()
        pwdelement = self.driver.find_element_by_class_name('Ypffh')
        pwdelement.clear()

        ok = False
        if type(comment) is list:
            ok = True

        for i in range(cont):

            if ok:
                while True:
                    text = f'@{random.choice(comment)[1]}'
                    if text != f'@{username}':
                        break

            else:
                text = comment

            print(f'[+] @{username} comentando {text}')
            pwdelement.send_keys(text)
            self.driver.find_element_by_class_name('X7cDz').submit()
            sleep(3)

        self.like()

    # curtir a publicação
    def like(self):
        curtir = self.driver.find_element_by_class_name('fr66n')
        svg = curtir.find_element_by_tag_name('svg')

        if svg.get_attribute('aria-label') == 'Curtir':
            curtir.click()

        sleep(2)

    # logout
    def logout(self):
        self.driver.get('https://www.instagram.com/accounts/logout/')
        sleep(2)

    def __init__(self, url, voltas, comments, texto='@', timeout=0):

        print('-'*50)

        self.options = webdriver.ChromeOptions()

        # Inicializa o webdriver
        self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.maximize_window()

        users = listlogins(conn)
        marcs = listpessoas(conn)

        # faz login
        for i in range(voltas):
            for c in users:

                if texto == '@':
                    if len(users) > 1:
                        text = users

                    else:
                        print('[-] Para comentar @bots deve cadastrar mais de uma conta')
                        text = input('[?] Novo texto do comentário: ')

                elif texto == '@@':
                    if len(marcs) > 1:
                        text = marcs

                    else:
                        print('[-] Para comentar @marcações deve cadastrar mais de uma conta')
                        text = input('[?] Novo texto do comentário: ')

                elif texto == '@@@':
                    if len(marcs+users) > 1:
                        text = marcs+users

                    else:
                        print('[-] Para comentar @marcações+bots deve cadastrar mais de uma conta')
                        text = input('[?] Novo texto do comentário: ')

                else:
                    text = texto

                try:
                    self.login(c[1], base64.b64decode(c[2]).decode())
                    self.comment(url, text, comments, c[1])
                except Exception as err:
                    print(f'Erro: {err}')
                print(f'[*] Aguardando timeout... ({timeout} segundos)')
                sleep(timeout)
                try:
                    self.logout()
                except Exception as err:
                    print(f'Erro: {err}')

        self.driver.quit()


if __name__ == '__main__':
    conn = sqlite3.connect('contas.db')

    createdb(conn)

    while True:
        command = input('[INSTABOT] >>> ')

        if command == 'list':
            print(' ID  |       USER       |  PASSWD')
            for i in listlogins(conn):
                print(f'  {i[0]}       {i[1]}     {base64.b64decode(i[2]).decode()}')
            print()

        if command == 'add':
            addlogin(conn, input('[?] Usuário : @'), input('[?] Senha: '))
            print('[+] Adicionado!')

        if command == 'del':
            dellogin(conn, input('[?] ID da conta: '))
            print('[+] Deletado!')

        if command == 'marc list':
            print(' ID  |       USER       ')
            for i in listpessoas(conn):
                print(f'  {i[0]}       {i[1]}')
            print()

        if command == 'marc add':
            addpessoa(conn, input('[?] Usuário : @'))
            print('[+] Adicionado!')

        if command == 'marc del':
            delpessoa(conn, input('[?] ID do nome de usuário: '))
            print('[+] Deletado!')

        if command == 'go':
            try:
                url = input('[?] URL do post: ')
                voltas = int(input('[?] Voltas: '))
                cmts = int(input('[?] Quantidade de comentários por usuário: '))
                texto = input('[?] Texto do comentário: ')
                timeout = input('[?] Timeout: ')
                if timeout == '':
                    timeout = 0
                else:
                    timeout = int(timeout)

                instabot(url, voltas, cmts, texto, timeout)
            except Exception as err:
                print(f'Erro: {err}')
            print('[+] FINALIZADO!')

        if command == 'exit':
            exit('Até a proxima soldado(a)!')
