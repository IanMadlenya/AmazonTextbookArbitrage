import requests
import bs4
import threading
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#AMAZON_URL = "https://www.amazon.com/s/search-alias%3Dtradein-aps&field-keywords={0}&page={1}"
AMAZON_URL = "https://www.amazon.com/s/ref=sr_nr_i_0?srs=9187220011&fst=as%3Aoff&rh=i%3Atradein-aps%2Ck%3A{0}%2Ci%3Astripbooks&page={1}"
ITEM_SELECTOR = ".s-item-container"
TRADE_IN_SELECTOR = ".a-color-price"
ITEM_SPECIFICS = ".a-text-left.a-col-right"
# Page count = [0], Publisher = [1], ISBN-100 = [2], ISBN-13 = [3]
BOOK_TITLE = ".s-access-title"
BOOK_COVER = ".cfMarker"
TRADE_IN_REVIEW_BOX = ".a-span-last"


def isTradeInEligible(item):
	# Determines if the item is trade in eligible or not
	return ('tradein' in item.select(TRADE_IN_REVIEW_BOX)[0])

def getPageCount(page):
	try:
		pageCount = int(page.select(".pagnDisabled")[0].getText())
	except:
		try:
			pageCount = int(re.findall("(\d+)", str(page.select("#pagn")[0].getText().replace("\n", " ")))[-1])
		except:
			pageCount = 1
	return pageCount


def grabPage(url):
	for i in range(3):
		res = requests.get(url, headers=headers, timeout=10)
		if res != None:
			break
	page = bs4.BeautifulSoup(res.text, 'lxml')
	try:
		pageNum = re.findall('page\S(\d+)', url)[0]
	except:
		pageNum = 1
	print("Grabbed: {} | Page: {}".format(page.title.string, pageNum))
	return page


class amazonTextbookDB(object):
	def __init__(self, arg):
		self.arg = arg
		self.database = []

	#def search(self, keyword):


	#def search(self, keyword):


if __name__ == '__main__':
	url = "https://www.amazon.com/s/ref=sr_nr_i_0?srs=9187220011&fst=as%3Aoff&rh=i%3Atradein-aps%2Ck%3Abiology%2Ci%3Astripbooks&keywords=biology&ie=UTF8&qid=1527811678"
	#url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=srs%3D9187220011%26search-alias%3Dtradein-aps&field-keywords=python+2&rh=i%3Atradein-aps%2Ck%3Apython+2"
	#url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=srs%3D9187220011%26search-alias%3Dtradein-aps&field-keywords=python+program&rh=i%3Atradein-aps%2Ck%3Apython+program"
	#url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=srs%3D9187220011%26search-alias%3Dtradein-aps&field-keywords=python+3&rh=i%3Atradein-aps%2Ck%3Apython+3"
	page = grabPage(url)
	print getPageCount(page)
	#print getResultCount(page).getText()
