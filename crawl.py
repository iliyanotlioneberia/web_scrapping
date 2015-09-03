from lxml import html
import requests
import json
import urllib2


class getFruits(object):

    def __init__(self):

        self.page = requests.get("http://www.sainsburys.co.uk/webapp/wcs/stores/servlet/CategoryDisplay?listView=true&or"
                                "derBy=FAVOURITES_FIRST&parent_category_rn=12518&top_category=12518&langId=44&beginInde"
                                "x=0&pageSize=20&catalogId=10137&searchTerm=&categoryId=185749&listId=&storeId=10151&pr"
                                "omotionId=#langId=44&storeId=10151&catalogId=10137&categoryId=185749&parent_category_r"
                                "n=12518&top_category=12518&pageSize=20&orderBy=FAVOURITES_FIRST&searchTerm=&beginIndex"
                                "=0&hideFilters=true")
        self.tree = html.fromstring(self.page.text)
        self.lista_products = list()
        self.lista_prices = list()
        self.lista_desc = list()
        self.lista_length = list()
        self.lista_results = list()

    def get_names(self):

        products = self.tree.xpath('//div[@class="productInfo"]/h3/a/text()')

        for i in products:
            if i == '\r\n\t                                    ':
                continue
            else:
                a = i.replace('\r\n\t                                        ', '')
                self.lista_products.append(a)

    def get_product_price(self):

        prices = self.tree.xpath('//p[@class="pricePerUnit"]/text()')

        for i in prices:
            if i == '\r\n':
                continue
            else:
                i1 = i.encode('utf-8')
                a = i1.replace('\r\n\xc2\xa3', '')
                self.lista_prices.append(a)

    def get_urls_for_each_page(self):

        urls = self.tree.xpath('//div[@class="productInfo"]/h3/a/@href')

        for i in urls:
            response = urllib2.urlopen(i)
            page2 = requests.get(i)
            tree2 = html.fromstring(page2.text)
            desc = tree2.xpath('//div[@class="productText"]/p/text()')
            if desc:
                self.lista_desc.append(desc[0])
                self.lista_length.append(len(response.read()))

    def wrap(self):

        pp = zip(self.lista_products, self.lista_prices, self.lista_desc, self.lista_length)

        for i in pp:
            d = dict(title=i[0], unit_price=i[1], size=i[3], description=i[2])
            self.lista_results.append(d)

        total_price_units = 0

        for i in self.lista_prices:
            total_price_units += float(i)

        final_dict = dict(results=self.lista_results, total=total_price_units)

        json_file = json.dumps(final_dict)

        return json_file


# SIMPLE UNIT TEST
def test_json(data):
    import json
    try:
        json.loads(data)
        print "valid JSON"
    except ValueError:
        print "not a valid JSON"
