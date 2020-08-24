from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from time import sleep
import sqlite3
import base64
import random

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

        for i in range(cont):
            print(f'[+] @{username} comentando {comment}')
            pwdelement.send_keys(comment)
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

    def __init__(self, db, url, voltas, comments, texto='@', timeout=0):

        print('-'*50)

        self.options = webdriver.ChromeOptions()

        # Inicializa o webdriver
        self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.maximize_window()

        db.execute("SELECT * FROM login")
        users = db.fetchall()

        # faz login
        for i in range(voltas):
            for c in users:

                if texto == '@':
                    if len(users) > 1:
                        while True:
                            text = f'@{random.choice(users)[1]}'
                            if text != f'@{c[1]}':
                                break
                    else:
                        print('[-] Para comentar @s deve cadastrar mais de uma conta')
                        text = input('[?] Novo texto do comentário: ')
                else:
                    text = texto

                self.login(c[1], base64.b64decode(c[2]).decode())
                self.comment(url, text, comments, c[1])
                print(f'[*] Aguardando timeout... ({timeout} segundos)')
                sleep(timeout)
                self.logout()

        self.driver.quit()


if __name__ == '__main__':
    conn = sqlite3.connect('contas.db')
    sql = conn.cursor()

    sql.execute("CREATE TABLE IF NOT EXISTS login (id INTEGER PRIMARY KEY, user TEXT, pass TEXT)")

    while True:
        command = input('[INSTABOT] >>> ')

        if command == 'list':
            sql.execute("SELECT * FROM login")
            print(' ID  |       USER       |  PASSWD')
            for i in sql.fetchall():
                print(f'  {i[0]}       {i[1]}     {base64.b64decode(i[2]).decode()}')
            print()

        if command == 'add':
            query = f"INSERT INTO login (user, pass) VALUES ('{input('[?] Usuário (não o email) : ')}', '{base64.b64encode(input('[?] Senha: ').encode()).decode()}');"
            sql.execute(query)
            print('[+] Adicionado!')
            conn.commit()

        if command == 'del':
            query = f"DELETE FROM login WHERE id = {input('[?] ID da conta: ')};"
            sql.execute(query)
            print('[+] Deletado!')
            conn.commit()

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

                instabot(sql, url, voltas, cmts, texto, timeout)
            except Exception as err:
                print(f'Erro: {err}')
            print('[+] FINALIZADO!')

        if command == 'exit':
            exit('Até a proxima soldado(a)!')
