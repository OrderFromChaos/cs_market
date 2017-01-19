# cs_market

NOTE: The use of any of this code may violate the Steam TOS, as the TOS bans the use of botting to automate market processes. This was written as a code experiment to test my mettle on auto-browsing websites and pulling data from real sources. As such, probably avoid using your own account or buying anything while testing this repo.

The code here is split into three versions, each of which represent my progress on getting better at software design and various Python libraries.

Version 1 is the first version, which uses [Steam's backend](http://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=StatTrak%E2%84%A2%20P250%20%7C%20Steel%20Disruption%20%28Factory%20New%29) to grab prices. It uses [lxml](http://lxml.de/) and [requests](http://docs.python-requests.org/en/master/) exclusively, and can update individual item price listings every 5 seconds.

Version 2 uses [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to augment lxml, and pulls data from the actual community market webpages. However, it is much slower than v1, and can update individual item price listings every 12.5 seconds.

Version 3 uses [Selenium](http://www.seleniumhq.org/) and [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/) to navigate around the listings on the Steam website, which gets rid of a lot of the weird issues in the previous versions. The code is robust and stable over long periods of searching (ie hours).
