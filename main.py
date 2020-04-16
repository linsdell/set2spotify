from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

site= "https://www.1001tracklists.com/tracklist/1gsnzruk/quivver-the-anjunadeep-edition-271-2019-09-26.html"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page)
print(soup)

stat_table = soup.find(class_="tlToogleData")
stat_table_data = stat_table.tbody.find_all("tr")
