from unicodedata import decimal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
 
#WebScrapper Searching GPU prices first page only
def GetPrice(text):
    result = ''
    resultFloat = 0
    array = list(text)
    for item in array:
        if item.isnumeric() or item == ',':
            if item == ',':
                result += '.'
            else:
                result += item
    try:
        resultFloat = float(result)
    except Exception as ex:
        print(ex)
        result = 0
        
    return resultFloat
 
# create webdriver object
optionsDriver = Options()
optionsDriver.headless = True
driver = webdriver.Firefox(options=optionsDriver)
driver.get("https://www.terabyteshop.com.br/hardware/placas-de-video")

priceLimit = 3000

items = driver.find_elements(By.CLASS_NAME,'commerce_columns_item_inner')
print('\nTerabyte GPU-------------------------------------------------')
for item in items:  
    blockProductName = item.find_element(By.CLASS_NAME,'commerce_columns_item_caption')
    blockProductInfo = item.find_element(By.CLASS_NAME,'commerce_columns_item_info')
    productName = blockProductName.find_element(By.CLASS_NAME,'prod-name')
    productOldPrice = blockProductInfo.find_element(By.CLASS_NAME,'prod-old-price')
    productNewPrice = blockProductInfo.find_element(By.CLASS_NAME,'prod-new-price')
    productJuros = blockProductInfo.find_element(By.CLASS_NAME,'prod-juros')
    
    if priceLimit >= GetPrice(productOldPrice.text) or priceLimit >= GetPrice(productNewPrice.text):
        print(f'Product: {productName.text}'+
            f'\nPrices: {productOldPrice.text} {productNewPrice.text} {productJuros.text}')
        #print(f'Prices Only: {GetPrice(productOldPrice.text)} {GetPrice(productNewPrice.text)}')
    
driver.get("https://www.kabum.com.br/hardware/placa-de-video-vga")
items = driver.find_elements(By.CLASS_NAME,'productCard')
print('\nKabum GPU-------------------------------------------------')
for item in items:  
    blockProductName = item.find_element(By.CLASS_NAME,'nameCard')
    blockProductInfo = item.find_element(By.CLASS_NAME,'priceCard')
    if priceLimit >= GetPrice(blockProductInfo.text):
        print(f'Product: {blockProductName.text}'+
            f'\nPrices: {blockProductInfo.text}')
        #print(f'Prices Only: {GetPrice(blockProductInfo.text)}')
    
driver.quit()