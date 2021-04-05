from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class locales(Item):
    link = Field()
    precio= Field()
    metros_2= Field()
    direccion= Field()
    direccion2= Field()


class Pisos(CrawlSpider):
    name = 'Pisos'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 50
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = [ 'www.pisos.com']

    start_urls = ['https://www.pisos.com/alquiler/local_comercial-madrid/']

    download_delay = 1

    rules = (
        # Paginación
        Rule(
            LinkExtractor(
                allow= "/local_comercial-madrid/\d+/"
                # deny=(r'?pagenumber=',)

            ), follow=True
        ),
        # Detalle productos
        Rule(
            LinkExtractor(
                allow=(r'/alquilar/local_comercial-', ),
                # deny=(r'https://www.atrapalo.com/actividades/madrid/',)
                restrict_xpaths = ['//div[@id="parrilla"]//div[contains(@class,"row") and contains(@class,"clearfix")]']

            ), follow= True, callback="parse_items"
        ),
    )


    def parse_items(self,response):
        item= ItemLoader(locales(),response)
        item.add_value("link",response.request.url)
        item.add_xpath("precio",'(//div[@class="priceBox-price"]/span)[1]/text()')
        item.add_xpath("metros_2",'(//div[@class="basicdata-info"]//div[@class="basicdata-item"])[1]/text()')
        item.add_xpath("direccion",'//div[@class="maindata-info"]//h1/text()')
        item.add_xpath("direccion2",'//div[@class="maindata-info"]//h2/text()')

        yield item.load_item()
