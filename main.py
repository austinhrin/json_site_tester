#### preinstalled python dependancies
import webbrowser
from time import sleep
import random
from datetime import datetime
from importlib import util
import json
import sys
import os

### pip installed dependancies
# https://pypi.org/project/webdriver-manager/
webdriver_manager_ = util.find_spec('webdriver_manager')
found_webdriver_manager = webdriver_manager_ is not None
if found_webdriver_manager == True:
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options as coptions
    from selenium.webdriver.firefox.options import Options as foptions
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
else:
    print('could not find webdriver_manager!')

TEST_LOG_FILE = 'test.log'
def log(text):
    print(text)
    with open(TEST_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write('\n')
        f.write(str(text))

def run_selenium(test, selenium_browser):
    try:
        if selenium_browser == 'chrome':
            chrome_options = coptions()
            chrome_options.page_load_strategy = 'normal'
            chrome_options.add_experimental_option('detach', True)
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-certificate-errors-spki-list')
            chrome_options.add_argument('--ignore-ssl-errors')
            #chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            # service = Service(executable_path='C:\Program Files\Chrome Driver\chromedriver.exe', options=chrome_options)
            driver = webdriver.Chrome(options=chrome_options)
        elif selenium_browser == 'firefox':
            firefox_options = foptions()
            # firefox_options = webdriver.FirefoxProfile()
            firefox_options.page_load_strategy = 'normal'
            firefox_options.accept_untrusted_certs = True
            driver = webdriver.Firefox(options=firefox_options)
        driver.get(test['website'].lower())
        # wait for website to fully load
        sleep(3)
        for command in test['selenium_commands']:
            if command['type'] == 'input':
                input_field = driver.find_element('xpath', command['xpath'])
                input_field.send_keys(test[command['input_variable']])
            elif command['type'] == 'button':
                button = driver.find_element('xpath', command['xpath'])
                button.click()
            elif command['type'] == 'wait':
                sleep(int(command['duration']))
            elif command['type'] == 'execjs':
                driver.execute_script(command['js'])
            elif command['type'] == 'newtab':
                driver.execute_script("window.open('');")
            elif command['type'] == 'closetab':
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
            elif command['type'] == 'openurl':
                sleep(1)
                driver.get(test[command['input_variable']])
        # success_checks
        if 'success_checks' in test:
            checks = test['success_checks']
            for check in checks:
                if 'xpath' in check:
                    text = driver.find_element('xpath', check['xpath']).text
                elif 'cookie' in check:
                    cookies = driver.get_cookies()
                    for cookie in cookies:
                        if cookie['name'] == check['cookie']:
                            text = cookie['value']
                # print(text)
                if 'eq' in check:
                    # assert check['eq'].lower() == text.lower()
                    if check['eq'].lower() == text.lower():
                        log(f'PASSED "eq": {check["eq"].lower()}')
                    else:
                        log(f'FAILED: "{check["eq"].lower()}" NOT EQ "{text.lower()}"')
                if 'noteq' in check:
                    # assert check['noteq'].lower() != text.lower()
                    if check['noteq'].lower() != text.lower():
                        log(f'PASSED "noteq": {check["noteq"].lower()}')
                    else:
                        log(f'FAILED: "{check["noteq"].lower()}" EQ "{text.lower()}"')
                if 'in' in check:
                    # assert check['in'].lower() in text.lower()
                    if check['in'].lower() in text.lower():
                        log(f'PASSED "in": {check["in"].lower()}')
                    else:
                        log(f'FAILED: "{check["in"].lower()}" NOT IN "{text.lower()}"')
                if 'notin' in check:
                    # assert check['notin'].lower() not in text.lower()
                    if check['notin'].lower() not in text.lower():
                        log(f'PASSED "notin": {check["notin"].lower()}')
                    else:
                        log(f'FAILED: "{check["notin"].lower()}" IN "{text.lower()}"')
        driver.close()
        return True
    except Exception as e:
        try:
            driver.close()
        except NameError:
            pass
        log(e)
        log(f'Was not able to test {test}')
        return False

def main():
    # browser to use for selenium: chrome or firefox
    selenium_browser = ''
    file_list = []
    # name of python script is always first arg
    if len(sys.argv) == 2:
        file_list.append(sys.argv[1])

    # get list of files in json folder
    if len(sys.argv) != 2:
        path = os.getcwd()
        for root, _dirs, files in os.walk(os.path.join(path, 'json')):
            for file in files:
                if file.endswith('.json'):
                    file_list.append(os.path.join(root,file))

    for file in file_list:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                tests = json.load(f)
            for test in tests:
                test_num = 0
                log(f'Testing: {file} {test}')
                if selenium_browser == '':
                    log('Testing on Chrome')
                    run_selenium(tests[test], 'chrome')
                    log('Testing on Firefox')
                    run_selenium(tests[test], 'firefox')
                else:
                    run_selenium(tests[test], selenium_browser)
                test_num += 1 
        except FileNotFoundError:
            log(f'Failed to open json file {file}')

if __name__== '__main__':
    if found_webdriver_manager is True:
        main()
