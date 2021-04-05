from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
# from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
# from bs4 import BeautifulSoup

encabezados = {
    "USER_ARGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36" ,
}


class Pregunta(Item):
    id = Field()
    pregunta = Field()
    descripcion = Field()


class Stackoverflow(Spider):
    name = "miPrimerSpider"

    encabezados = {
        "USER_ARGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 "
                       "Safari/537.36"}

    start_urls = ['https://stackoverflow.com/questions']

    def parse(self, response):
        sel = Selector(response)
        preguntas = sel.xpath('//div[@id="questions"]//div[@class="question-summary"]')
        i=0
        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta)
            item.add_xpath('pregunta', './/h3/a/text()')
            item.add_xpath('descripcion', './/div[@class="excerpt"]/text()')
            item.add_value('id', i)
            i=i+1

            yield item.load_item()
