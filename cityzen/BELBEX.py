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


class BELBEX(CrawlSpider):
    name = 'BELBEX'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 50
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = [ 'belbex.com']

    start_urls = ['https://belbex.com/locales/madrid-provincia/alquiler/']

    download_delay = 1

    rules = (
        # Paginación
        Rule(
            LinkExtractor(
                allow= r"/pagina-\d+/"

            ), follow=True
        ),
        # Detalle productos
        Rule(
            LinkExtractor(
                # allow=(r'detalles\\/alquiler\\/', ),
                allow=(r'^(?=.*\bdetalles\b)(?=.*\balquiler\b)', ),
                deny=(r'^(?=.*\b/tel:\b)(?=.*\b/pagina-\d+/\b)',),
                # restrict_xpaths = ['//section[@class=class="placardsTab rightpanel showResults"]//ul//li//article//header//a']
                restrict_xpaths = ['//section[@class="placardsTab rightpanel showResults"]//ul//li//article//header//a']

            ), follow= True, callback="parse_items"
        ),
    )


    def parse_items(self,response):
        item= ItemLoader(locales(),response)
        item.add_value("link",response.request.url)
        item.add_xpath("precio",'//h2[@class="specs address"]/span[@class="addressDetails"]/span[@class="priceContainer"]/span[@class="totalPrice"]/text()')
        item.add_xpath("metros_2",'//h2[@class="specs address"]/span[@class="addressDetails"]/span[@class="sizeContainer"]/span[@class="sizeInfo"]/text()')
        item.add_xpath("direccion",'//div[@class="stickyAddress"]/div/h1//*/text()')

        yield item.load_item()
