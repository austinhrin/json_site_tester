#### preinstalled python dependancies
import webbrowser
from time import sleep
import random
from datetime import datetime
from importlib import util
import json

### pip installed dependancies
# https://pypi.org/project/webdriver-manager/
webdriver_manager_ = util.find_spec("webdriver_manager")
found_webdriver_manager = webdriver_manager_ is not None
if found_webdriver_manager == True:
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as coptions
    from selenium.webdriver.firefox.options import Options as foptions
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
else:
    print('Not importing selenium!')

### user created dependancies


# browser to use for selenium: chrome or firefox
selenium_browser = 'firefox'

# tests from json file
with open('tests.json', 'r') as f:
    data = json.load(f)

def run_selenium(test):
    if found_webdriver_manager == True:
        try:
            if selenium_browser == 'chrome':
                chrome_options = coptions()
                chrome_options.add_experimental_option("detach", True)
                driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
            elif selenium_browser == 'firefox':
                #firefox_options = foptions()
                #firefox_options.add_experimental_option("detach", True)
                driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
            driver.get(test['website'].lower())
            # wait for website to open
            sleep(4)
            for command in test['selenium_commands']:
                if command['type'] == 'input':
                    input_field = driver.find_element_by_xpath(command['xpath'])
                    input_field.send_keys(test[command['input_variable']])
                elif command['type'] == 'button':
                    button = driver.find_element_by_xpath(command['xpath'])
                    button.click()
            #driver.close()
        except:
            return 'Was not able to test ' + str(test)
    return 'found_webdriver_manager is False Selenium was not imported.'


test1 = run_selenium(data['login'])
print(test1)