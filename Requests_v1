#This one pulls from steam's internal JSON api. More information here: http://bit.ly/2iDja0Q
#I don't recommend using this one, but it is the second fastest of the three (v3, v1, then v2)

from lxml import html
import requests
import time

#These happened to be the items I owned at the time.
items = ['AUG | Bengal Tiger (Factory New)', 'StatTrak™ Music Kit | AWOLNATION, I Am', 'StatTrak™ Music Kit | Daniel Sadowski, Total Domination', 'StatTrak™ SG 553 | Cyrex (Well-Worn)', 'AWP | Sun in Leo (Factory New)', 'AWP | Phobos (Factory New)', 'AWP | Phobos (Minimal Wear)', 'Music Kit | Noisia, Sharpened', 'Music Kit | Mateo Messina, For No Mankind', 'AUG | Chameleon (Factory New)']
#I also had two arrays that 
long_list_items, high_hf_items = [], []

#Steam automatically temp bans you if you try to get more than 20 items per minute.
#60/20 = 3 seconds between requests, but things close to 3 seconds also seem to get banned.
#To be safe, I set this to 5. That means 5 seconds per item update.
wait = 5
analyze = long_list_items + high_hf_items + items

print("Expected time to run through this list:",wait*len(analyze),"seconds")

for i in analyze:
    #If your item name includes spaces, it will automatically be formatted correctly.
    url = "http://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name=" + i
    page = requests.get(url)
    tree = html.fromstring(page.content)
    text = tree.xpath('text()')
    
    editable = list(text[0])
    
    #Prevents errors if the JSON request fails:
    failed = False
    if len(editable) > 10:
        try:
            if editable[11] == 'f':
                print("Name of item spelled incorrectly. (",i,")")
                failed = True
            if editable[17] == 'v':
                print("\n","This item",i,"has no current price listed.")
                failed = True
        except:
            print("Well, this is a strange bug. Here's the info:")
            print(text)
            print(i)
    
    #If this happens, you probably got temp banned.
    if editable[0] == 'n':
        print("JSON request failed!")
        failed = True
        break
        
        
    if failed == False:
        try:
            #Makes data look nice:
            editable.remove(':')
            del editable[0:editable.index(':')+2]
            current = ''.join((editable[0:editable.index('\"')]))
            del editable[0:editable.index(':')+2]
            volume = ''.join(editable[0])
            del editable[0:editable.index(':')+2]
            median = ''.join(editable[0:editable.index('\"')])

            #calculates percentages to find out if it should display the value
            if current < median:
                state = 'BUY'
                percent = (1-float(current[1:len(current)])/float(median[1:len(median)]))*100
            elif current > median:
                state = 'SELL'
                percent = ((float(current[1:len(current)])/float(median[1:len(median)]))-1)*100
            else:
                state = 'NONE'
                percent = 0.0

            #If the percentage difference is over a certain value, the program will make buy/sell suggestions
            #In this case, the value is set to the break-even point for the CS:GO Community Market.
            if percent >= 15.0:
                print("")
                print(i,'\n','Current:',current,'Median:',median,'Volume:',volume)
                if state == 'BUY':
                    print(i,'\n','Current:',current,'Median:',median,'Volume:',volume)
                elif state == 'SELL' and i in items:
                    print('This item is a SELL, with a ',round(percent,3),'percent difference from normal')
                else:
                    print('|',end = '')
                    
                if i in items:
                    print('From items')
                if i in high_hf_items:
                    print('From high_hf_items')
                if i in long_list_items:
                    print('From long_list_items')

            else:
                #Progress bar to make it clear the program is running
                print('|',end = '')
        except ValueError:
            #Sometimes it would run into bugs during runtime, usually because the input
            #was highly different than expected. This accounts for that.
            print("Well, that is a strange bug. Here's the info about this.")
            print(text)
            print(i)
            
    time.sleep(wait)
    
print('\n',"Analysis finished!")
