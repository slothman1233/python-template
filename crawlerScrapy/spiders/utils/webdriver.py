from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

def select_assign(driver, id, value):
    '''
    select 选中赋值 
    '''
    try:
        SetPregnancy = driver.find_element(by=By.ID, value=id)
        # .send_keys('python')
        Select(SetPregnancy).select_by_index(value)
    except:
        return False


def input_assign(driver, id, value):
    '''
    input 赋值
    '''
    try:
        SetCalculatorPeMom = driver.find_element(
            by=By.ID, value=id)
        # .send_keys('python')
        SetCalculatorPeMom.send_keys(value)
    except:
        return False


def execute_script(driver, script):
    '''
    执行script
    '''
    driver.execute_script(script)
