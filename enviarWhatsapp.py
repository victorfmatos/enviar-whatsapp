from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

nome_do_grupo = ''  # nome do grupo que deseja enviar, sem emoji!!!
caminho_arquivo = r''  # caminho do arquivo que deseja enviar!!!
caminho_chrome = r''  # caminho da pasta copiada!!!

options = Options()
options.add_argument("profile-directory=Default")
options.add_argument("headless=new")
options.add_argument("start-maximized")
options.add_argument(rf"user-data-dir={caminho_chrome}")
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://web.whatsapp.com/")
while len(driver.find_elements(By.ID, 'side')) < 1:
    sleep(1)
print('Abriu o \033[32mWhatsapp\033[m.')
sleep(2)

SCROLL_PAUSE_TIME = 1

error = True
height = 400

while error:
    try:
        driver.find_element(
            By.XPATH, f'//span[contains(@title, "{nome_do_grupo}")]').click()
        error = False
    except NoSuchElementException:
        driver.execute_script(
            f'document.getElementById("pane-side").scrollTop = {height}')
        sleep(SCROLL_PAUSE_TIME)

        print('Procurando o \033[34mcontato\033[m.')
        if height >= driver.execute_script('return document.getElementById("pane-side").scrollHeight'):
            break

        height += 400


driver.find_element(By.XPATH, '//span[@data-icon="attach-menu-plus"]').click()
driver.find_element(
    By.XPATH, '//input[@accept="*"]').send_keys(caminho_arquivo)
sleep(2)
button_submit = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
driver.execute_script('arguments[0].click()', button_submit)
sent = False
sleep(1)
while not sent:
    if driver.find_elements(By.XPATH, '//span[@aria-label=" Pendente "]'):
        print('\033[33mEnviando\033[m.')
        sleep(1)
    else:
        print('\033[32mEnviado\033[m.')
        sent = True
sleep(1)
