from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Articulo(Item):
    link = Field()
    titulo = Field()
    precio = Field()
    descripcion = Field()


class Tripadvisor(CrawlSpider):
    name = 'Tripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 10
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['www.tripadvisor.es']
    start_urls = ['https://www.tripadvisor.es/Attraction_Products-g187514-a_sort.-d190143-Prado_National_Museum-Madrid.html']

    download_delay = 1

    rules = (
        # Paginación
        Rule(
            LinkExtractor(
                allow="?o=a\d+"
            ), follow=True
        ),
        # Detalle productos
        Rule(
            LinkExtractor(
                allow=r'Attraction_Review-g187514-',
                restrict_xpaths = ['//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]//a[@data-clicksource="HotelName"]'] #limitar el espectro de búsqueda

            ), follow=True, callback="parse_items"
        ),
    )

    def limpiar(self, texto):
        nuevotexto = texto.replace("\n", "").replace("\t", "").replace("\r", "")
        return nuevotexto

    def parse_items(self, response):
        item = ItemLoader(Articulo(), response)
        item.add_value("link", response.request.url)
        item.add_xpath('titulo', '//h1[@id="HEADING"]/text()')
        item.add_xpath('precio', '//div[@class="_80M-a_oA"]')
        item.add_xpath('descripcion', '//div[@class="RByRLEDA hasAvatar"]/text()')
        # item.add_xpath('amenities','//div[contains(@data-ssrev-handlers,"amenities")]//text()')

        yield item.load_item()
