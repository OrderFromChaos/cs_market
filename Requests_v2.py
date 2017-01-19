#This one pulls data from the actual steam webpages instead of the json API,
#Since the JSON api seemed to be returning some weird/wrong results sometimes.
#(Unfortunately, this implementation also has problems, as you'll see. This is fixed in v3.)

from lxml import html
import requests
from bs4 import BeautifulSoup
import time
import winsound

items = ['AUG | Bengal Tiger (Factory New)', 'StatTrak™ Music Kit | AWOLNATION, I Am', 'StatTrak™ Music Kit | Daniel Sadowski, Total Domination', 'StatTrak™ SG 553 | Cyrex (Well-Worn)', 'AWP | Sun in Leo (Factory New)', 'AWP | Phobos (Factory New)', 'AWP | Phobos (Minimal Wear)', 'Music Kit | Noisia, Sharpened', 'Music Kit | Mateo Messina, For No Mankind', 'AUG | Chameleon (Factory New)']
high_hf_items, long_list_items = [], []

#Note that if you're not logged in, Steam will show the prices of things in their native currencies.
#This is a problem for any USD analysis. To fix this, I had to convert the currencies.

previous_currencies = []
previous_rates = []

#The data is taken from Bloomberg instead of XE, since XE sells their data and doesn't take too
#kindly to people farming it without their consent.
def rate(ticker):
    if ticker in previous_currencies:
        return float(previous_rates[previous_currencies.index(ticker)])
    url = 'https://www.bloomberg.com/quote/' + ticker + 'USD:CUR'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    text = tree.xpath('//*[@id="content"]/div/div/div[1]/div/div[4]/div[2]/text()') #Location of price data
    previous_currencies.append(ticker)
    previous_rates.append(text[0])
    return float(text[0])

#Two annoyingly long functions to deal with the horrible formatting of steam currencies.
def strip_non_numbers(b):
    #This removes the useless stuff that bs4 finds before doing the currency conversion. This ensures
    # the only things in the string are numbers, spaces, and currency symbols.
    while '\t' in b:
        del b[b.index('\t')]
    while '\r' in b:
        del b[b.index('\r')]
    while '\n' in b:
        del b[b.index('\n')]
    while '-' in b:
        del b[b.index('-')]
    while ' ' in b:
        del b[b.index(' ')]
    return b

def make_nice(c,preservelastcomma):
    
    if preservelastcomma == 1:
        while ',' in c:
            if c.count(',') == 1:
                c[c.index(',')] = '.'
                break
            else:
                del c[c.index(',')]
                
    elif preservelastcomma == 0:
        while ',' in c:
            del c[c.index(',')]
            
    else:
        #This is specifically for Columbian and Chilean Pesos.
        while ',' in c:
            c[c.index(',')] = '.'
        while '.' in c:
            del c[c.index('.')]
        while ',' in c:
            c[c.index(',')] = '.'
            
    #Just as a final checkup
    while c.count('.') > 1:
        del c[c.index('.')]
    
    return c

analyze = items + high_hf_items + long_list_items
#Unfortunately, the wait time for this is like a minimum of 10 seconds. So this is an extremeeeeely slow implementation.
wait = 12.5
noprice = 0

print("Expected time to run though list is", wait*len(analyze), "seconds")

for i in analyze:
    #Music kits don't have individual sale listings.
    if "Music Kit" in i:
        print("Music Kit Skipped.")
        pass
    else:
        url = 'http://steamcommunity.com/market/listings/730/' + i
        data = requests.get(url).content
        soup = BeautifulSoup(data,'lxml')
        prices = soup.findAll('span', class_='market_listing_price market_listing_price_with_fee')

        newprices = []
        for j in prices[:3]: #the total length is 10, but it's not necessary to know all of them.
            base = list(list(j)[0])
            #Now to convert currencies.

            found = False
            
            # -------------------------------------- CURRENCIES --------------------------------------
            #list of current unique triggers:
            # 8: $,S,¥,₩,N,P,R,£,฿,₹
            # 9: $,M,D,H,L,O,p
            # len-6: €,r,L,X
            # len-7: б
            # So yeah, Steam is really bad about making nice, reasonable currency listings.
            
            base = strip_non_numbers(base)
            
            if base == ['S', 'o', 'l', 'd', '!']:
                #Someone bought it between when the page was loaded and when the data was gathered. Impressive...
                found = True
            
            # -------------------------------------- USD (US Dollar: $) --------------------------------------
            if base[0] == '$':
                base = make_nice(base[1:],0)
                newprices.append(float(''.join(base)))
                found = True

            
            if found == False and base[0] == 'R':
            # -------------------------------------- BRL (Brazilian Real: R$) --------------------------------------
                if base[1] == '$':
                    base = make_nice(base[2:],1)
                    newprices.append(round(float(''.join(base))*rate('BRL'),2))
                    found = True
            # -------------------------------------- MYR (Malaysian Ringgit: RM) --------------------------------------
                elif base[1] == 'M':
                    base = make_nice(base[2:],1)
                    newprices.append(round(float(''.join(base))*rate('MYR'),2))
                    found = True
            # -------------------------------------- IDR (Indonesian Rupiah: Rp) --------------------------------------
                elif base[1] == 'p':
                    if '.' not in base: #This adds a period in the proper place if there isn't one already.
                        base.insert(len(base)-3,'.')
                    base = make_nice(base[2:],0)
                    newprices.append(round(float(''.join(base))*rate('IDR'),2))
                    found = True
            # -------------------------------------- ZAR (South African Rand: R)
                else:
                    base = make_nice(base[1:],0)
                    newprices.append(round(float(''.join(base))*rate('ZAR'),2))
                    found = True

            # -------------------------------------- EUR (Euro: €) --------------------------------------
            if found == False and base[len(base)-1] == '€':
                eurobase = base[:base.index('€')]
                eurobase = make_nice(eurobase,1)
                newprices.append(round(float(''.join(eurobase))*rate('EUR'),2))
                found = True

            # -------------------------------------- RUB (Russian Ruble: pуб) --------------------------------------
            if found == False and base[len(base)-2] == 'б':
                rublebase = base[:base.index('p')]
                rublebase = make_nice(rublebase,1)
                newprices.append(round(float(''.join(rublebase))*rate('RUB'),2))
                found = True

            # -------------------------------------- SGD (Singaporean Dollar: S$) --------------------------------------
            if found == False and base[0] == 'S':
                base = make_nice(base[2:],0)
                newprices.append(round(float(''.join(base))*rate('SGD'),2))
                found = True

            # -------------------------------------- CNY (Chinese Yuan: ¥) --------------------------------------
            if found == False and base[0] == '¥':
                base = make_nice(base[1:],0)
                newprices.append(round(float(''.join(base))*rate('CNY'),2))
                found = True

            # -------------------------------------- NOK (Swedish Krona: kr) --------------------------------------
            if found == False and base[len(base)-1] == 'r':
                kronabase = base[:base.index('k')]
                kronabase = make_nice(kronabase,1)
                newprices.append(round(float(''.join(kronabase))*rate('NOK'),2))
                found = True

            # -------------------------------------- TRY (Turkish Lira: TL) --------------------------------------
            if found == False and base[len(base)-1] == 'L':
                lirabase = base[:base.index('T')]
                lirabase = make_nice(lirabase,1)
                newprices.append(round(float(''.join(lirabase))*rate('TRY'),2))
                found = True

            # -------------------------------------- KRW (Korean Won: ₩) --------------------------------------
            if found == False and base[0] == '₩':
                base = make_nice(base[1:],0)
                newprices.append(round(float(''.join(base))*rate('KRW'),2))
                found = True

            # -------------------------------------- CAD (Canadian Dollar: CDN$) --------------------------------------
            if found == False and base[1] == 'D':
                base = make_nice(base[4:],0)
                newprices.append(round(float(''.join(base))*rate('CAD'),2))
                found = True

            # -------------------------------------- CHF (Swiss Franc: CHF) --------------------------------------
            if found == False and base[1] == 'H':
                base = make_nice(base[3:],0)
                newprices.append(round(float(''.join(base))*rate('CHF'),2))
                found = True
                
            # -------------------------------------- NZD (New Zealand Dollar: NZ$) --------------------------------------
            if found == False and base[0] == 'N':
                base = make_nice(base[3:],0)
                newprices.append(round(float(''.join(base))*rate('NZD'),2))
                found = True
            
            # -------------------------------------- PHP (Phillipines Peso: P) --------------------------------------
            if found == False and base[0] == 'P':
                base = make_nice(base[1:],0)
                newprices.append(round(float(''.join(base))*rate('PHP'),2))
                found = True
            
            # -------------------------------------- GBP (British Pounds: £) --------------------------------------
            if found == False and base[0] == '£':
                    base = make_nice(base[1:],0)
                    newprices.append(round(float(''.join(base))*rate('GBP'),2))
                    found = True
            
            # -------------------------------------- CLP (Chilean Peso: CLP$) --------------------------------------
            if found == False and base[1] == 'L':
                    base = make_nice(base[4:],2)
                    print("CLP",base)
                    newprices.append(round(float(''.join(base))*rate('CLP'),2))
                    found = True
            
            # -------------------------------------- COP (Columbian Peso: COL$) --------------------------------------
            if found == False and base[1] == 'O':
                    base = make_nice(base[4:],2)
                    newprices.append(round(float(''.join(base))*rate('COP'),2))
                    found = True
            
            # -------------------------------------- MXN (Mexican Peso: MEX$) --------------------------------------
            if found == False and base[2] == 'X':
                    base = make_nice(base[4:],0)
                    newprices.append(round(float(''.join(base))*rate('MXN'),2))
                    found = True
            
            # -------------------------------------- THB (Thai Baht: ฿) --------------------------------------
            if found == False and base[0] == '฿':
                    base = make_nice(base[1:],0)
                    newprices.append(round(float(''.join(base))*rate('THB'),2))
                    found = True
            
            # -------------------------------------- INR (Indian Rupee: ₹) --------------------------------------
            if found == False and base[0] == '₹':
                    base = make_nice(base[1:],0)
                    newprices.append(round(float(''.join(base))*rate('INR'),2))
                    found = True

            if found == False:
                #Rupees may activate this one. Keep on the lookout...
                print('\n',"Well! There's a currency you didn't account for. Check this link:")
                print(url)
                print(base)
            else:
                noprice = 0
        
        #This will activate if it finds two good prices.
        #Be warned! It will beep when it ends.
        if len(newprices) >= 2:
            print(i, newprices, str(round(((newprices[1]/newprices[0])-1)*100,2)) + '%')
            if newprices[0]*1.15 < newprices[1]:
                print("This is a definite buy.",'\n')
                #print(i,newprices,str(round(((newprices[1]/newprices[0])-1)*100,2)) + '%')
                winsound.Beep(2500,250)
            else:
                #print('|', end='')
                pass
            if round(((newprices[1]/newprices[0])-1)*100,2) < -5 or round(((newprices[1]/newprices[0])-1)*100,2) > 100:
                print('This percent is weird.')#, #str(round(((newprices[1]/newprices[0])-1)*100,2)) + '%')
                #print(i)
                print(prices)
            
        else:
            #This will activate if there's only one price for the item or if you're temp banned.
            print('\n',"This item has no prices!")
            print(i)
            noprice += 1
            if noprice == 2:
                print("Hit two consecutive no-prices. Ergo program quit.")
                break

        time.sleep(wait)

print('\n',"Analysis finished!")
