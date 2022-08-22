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
    if result != '':
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

priceLimit = 2500

items = driver.find_elements(By.CLASS_NAME,'commerce_columns_item_inner')
print('\nTerabyte GPU-------------------------------------------------')
for item in items:  
    try:
        blockProductName = item.find_element(By.CLASS_NAME,'commerce_columns_item_caption')
        blockProductInfo = item.find_element(By.CLASS_NAME,'commerce_columns_item_info')
        productName = blockProductName.find_element(By.CLASS_NAME,'prod-name')
        #productOldPrice = blockProductInfo.find_element(By.CLASS_NAME,'prod-old-price')
        productNewPrice = blockProductInfo.find_element(By.CLASS_NAME,'prod-new-price')
        productJuros = blockProductInfo.find_element(By.CLASS_NAME,'prod-juros')
        
        #priceOld = GetPrice(productOldPrice.text) 
        priceNew = GetPrice(productNewPrice.text)
        
        inRange = 0 
        #if priceOld > 0 :
            #if priceLimit >= priceOld:
                #inRange = 1
        if priceNew > 0 :
            if priceLimit >= priceNew:
                inRange = 1
                
        if inRange == 1:
            print(f'Product: {productName.text}'+
                f'\nPrices: {productNewPrice.text} {productJuros.text}')
    except:
        print('An error ocurred.')
        
driver.get("https://www.kabum.com.br/hardware/placa-de-video-vga?page_size=100&sort=most_searched")
items = driver.find_elements(By.CLASS_NAME,'productCard')
print('\nKabum GPU-------------------------------------------------')
for item in items:  
    try:
        blockProductName = item.find_element(By.CLASS_NAME,'nameCard')
        blockProductInfo = item.find_element(By.CLASS_NAME,'priceCard')
        price = GetPrice(blockProductInfo.text)
        if price > 0 :
            if priceLimit >= price:
                print(f'Product: {blockProductName.text}'+
                    f'\nPrices: {blockProductInfo.text}')
    except:
        print('An error ocurred.')
    
driver.quit()