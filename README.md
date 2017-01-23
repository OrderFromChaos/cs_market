# cs_market
###NOTE: The use of any of this code may violate the Steam TOS.

The Steam TOS bans the use of botting to automate market processes. This was written as a code experiment to test my mettle on auto-browsing websites and pulling data from real sources. This code does not automate buying or selling, only pulling information (at a slow rate) from the Steam Marketplace. Either way, I suggest avoiding using your own account or buying anything while testing this repo.

The code here is split into three versions, each of which represent my progress on getting better at software design and various Python libraries.

----------------------------------------------------------------------------------------------------------------------------------------
####Version 1
Version 1 is the first version, which uses [Steam's backend](http://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=StatTrak%E2%84%A2%20P250%20%7C%20Steel%20Disruption%20%28Factory%20New%29) to grab prices. It uses [lxml](http://lxml.de/) and [requests](http://docs.python-requests.org/en/master/) exclusively, and can update individual item price listings every 5 seconds. Steam's backend produces JSONs like the following:
```
{"success":true,"lowest_price":"$1.28","volume":"46","median_price":"$1.26"}
```

----------------------------------------------------------------------------------------------------------------------------------------
####Version 2: More robust data
Version 2 uses [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to augment lxml, and pulls data from the actual community market webpages, making the data more robust. However, it is much slower than v1, and can update individual item price listings every 12.5 seconds. It also has a rather messy original web data pull, which looks like this:
```
[<span class="market_listing_price market_listing_price_with_fee">
						CDN$ 26.00					</span>, <span class="market_listing_price market_listing_price_with_fee">
						18,72€					</span>, <span class="market_listing_price market_listing_price_with_fee">
						$21.85					</span>, <span class="market_listing_price market_listing_price_with_fee">
						CHF 57.50					</span>, <span class="market_listing_price market_listing_price_with_fee">
						57,50€					</span>, <span class="market_listing_price market_listing_price_with_fee">
						CDN$ 98.99					</span>]
```

----------------------------------------------------------------------------------------------------------------------------------------
####Version 3: Faster and more robust data
Version 3 uses [Selenium](http://www.seleniumhq.org/) and [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) to navigate around the listings on the Steam website, which gets rid of a lot of the weird issues in the previous versions. The code is robust and stable over long periods of searching (ie hours). The pages it searches over are price descending, factory new only by default. Here is an example of how it searches:
![Main directory](http://i.imgur.com/LJDPVWz.png)
First, it goes to the main directory page. Then it selects the first item, saving the directory page url in memory. It looks at the item page:
![Item photo](http://i.imgur.com/kl6GfNW.png)
![Item price listing](http://i.imgur.com/JuSwxl9.png)
Then grabs the price information from the listing on that page, putting it into a handy array.

The program then navigates all the way through the directory page, selecting each item. Once it reaches the end (after 10 items), it moves up or down a page by clicking the side arrows based on the original parameters it was given.

All price data is printed to standard out, but it would easy to switch it to outputting to a text file. The final data looks like this:
```
2. StatTrak™ MAC-10 | Ultraviolet (Factory New) 
 ['9,69€', '$10.35', '11,73€', '12,30€', 'CDN$ 17.25', '$12.97', '₩ 15,202.21', '¥ 89.33', '850 pуб.', '£12.35']
```
Although it is currently in local currency, there are plans to figure out a good way to make it show USD. One could be cribbing the currency converter from v2 (with a bit of rewriting, of course). Also, a more trusted account should have it in USD by default.
