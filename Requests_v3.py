#The best of them yet. Still in progress, but very functional as is.
#This one uses Selenium's Chromedriver to automate browser searching for prices.
#Note that depending on your account's status, it may return USD or local prices.

from selenium import webdriver
import sys
import time

#Initial conditions
#Here, you set the page range that you want. This page range will include the start and end pages and can go up or down.
general_url = 'http://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
initial_page = 50
final_page = 40
i_url = general_url + str(initial_page) + '_price_desc'
f_url = general_url + str(final_page) + '_price_desc'

addor = 0
if initial_page < final_page:
    addor = 1
else:
    addor = -1

print(addor)
print(i_url)
print(f_url)

browser = webdriver.Chrome(r'C:\Users\Syris Norelli\Downloads\ChromeDriver\ChromeDriver.exe') #Your directory here.

#Import data cleaning functions

def cleanListing(mess):
    mess = mess[mess.index('\n')+1:]
    prices = []
    ohman = 0
    #Extremely sloppy implementation; later I intend to figure out a more Pythonic way of doing things.
    while '\n' in mess:
        for mess_iterator in range(3):
            mess = mess[mess.index('\n')+1:]
            #This catches the file reader if it runs into the end of file before expected.
            if mess.strip() == 'Counter-Strike: Global Offensive':
                ohman = 1
                break
        if ohman == 1:
            break
        prices.append(mess[:mess.index('\n')])
        mess = mess[mess.index('\n')+1:]
        
    return prices

def cleanName(name):
    for nameiterator in range(3):
        name = name[name.index('\n')+1:]
    name = name[:name.index('\n')]
    return name

#Login
login_url = r'https://store.steampowered.com//login/'
browser.get(login_url)
time.sleep(5)
username = ''
password = ''
username_box = browser.find_element_by_css_selector('#input_username')
password_box = browser.find_element_by_css_selector('#input_password')
username_box.send_keys(username)
password_box.send_keys(password)

time.sleep(5) #Never can be too safe with inputting too fast.

sign_in = browser.find_element_by_css_selector('#login_btn_signin > button')
sign_in.click()

time.sleep(5)

itemno = 1
#Switching directory pages
for pageno in range(initial_page, final_page+addor ,addor):
    print('----------Page Number: ' + str(pageno) + ' ----------')
    page_url = general_url + str(pageno) + '_price_desc'
    #Navigating single directory page
    for directorypage in range(10):
        browser.get(page_url)

        #Select item in directory + get item name, then go to page
        browser.implicitly_wait(3)
        current_item = browser.find_element_by_css_selector('#result_' + str(directorypage))
        item_name = current_item.text
        item_name = cleanName(item_name)
        time.sleep(3)
        current_item.click()

        #Get price data
        browser.implicitly_wait(10)
        full_listing = browser.find_element_by_css_selector('#searchResultsRows').text
        itemized = cleanListing(full_listing)
        print(str(itemno) + '. ' + item_name,'\n', itemized)
        itemno += 1
        time.sleep(3)
        
    browser.get(page_url)
    time.sleep(3)
    if addor < 0:
        prevarrow = browser.find_element_by_css_selector('#searchResults_btn_prev')
        prevarrow.click()
    if addor > 0:
        nextarrow = browser.find_element_by_css_selector('#searchResults_btn_next')
        nextarrow.click()
    
    print('\n')

