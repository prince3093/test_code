import pandas as pd
import time
from selenium import webdriver

def record_processing():
    df = pd.read_csv("pharma.csv")
    df.loc[:, ~df.columns.str.contains('^Unnamed')]
    for i in range (len(df)):
        Name = df.loc[i, "Name"]
        Phone = (df.loc[i, "Phone"])
        Rating = int(df.loc[i, "Rating"])
        Address  = df.loc[i, "Address"]
        Zip = str(df.loc[i, "zip"])
    
        a=driver.find_element_by_xpath("//input[@placeholder='Name']")
        a.send_keys(Name)
        
        b = driver.find_element_by_xpath('//*[@id="c-1-248"]')
        b.send_keys(Phone)  
        
        c=  driver.find_element_by_xpath('//*[@id="c-2-9"]')
        c.send_keys(Address)   
        
        d =  driver.find_element_by_xpath('//*[@id="c-6-9"]')
        d.send_keys(Zip)
        
        if Rating == 1:
            driver.find_element_by_css_selector("input#c-9-4").click()
        if Rating == 2:
            driver.find_element_by_css_selector("input#c-9-5").click()
        if Rating == 3:
            driver.find_element_by_css_selector("input#c-9-6").click()
        if Rating == 4:
            driver.find_element_by_css_selector("input#c-9-7").click()
        if Rating == 5:
            driver.find_element_by_css_selector("input#c-9-8").click()   
    
        driver.find_element_by_xpath('//*[@id="c-submit-button"]').click()
        time.sleep(2)
        driver.refresh()

# Open Chrome and maximizing
driver = webdriver.Chrome('.\chromedriver.exe')
driver.maximize_window()
    
# Open Shell website
driver.get('https://www.cognitoforms.com/NirajGupta/VizagPharamacyRegistration')
time.sleep(10)

record_processing()

driver.quit()