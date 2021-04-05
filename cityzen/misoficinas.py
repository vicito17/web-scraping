from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Oficina(Item):
    link = Field()
    titulo = Field()
    precio= Field()
    descripcion = Field()
    metros_2= Field()
    direccion= Field()


class Misoficinas(CrawlSpider):
    name = 'misoficinas'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 50
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = [ 'www.misoficinas.es']

    start_urls = ['https://www.misoficinas.es/alquiler/locales/madrid']

    download_delay = 1

    rules = (
        # Paginación
        Rule(
            LinkExtractor(
                allow= r"pagenumber="
                # deny=(r'?pagenumber=',)

            ), follow=True
        ),
        # Detalle productos
        Rule(
            LinkExtractor(
                allow=(r'/id/', ),
                restrict_xpaths = ['//section[@class="s-property-list"]//div[@class="col col-lg-9"]//div[@class="c-property-list-item__content"]//div//a']

            ), follow= True, callback="parse_items"
        ),
    )


    def parse_items(self,response):
        item= ItemLoader(Oficina(),response)
        item.add_value("link",response.request.url)
        item.add_xpath("titulo",'//header[@id="single__header"]/div/h1/text()')
        item.add_xpath("precio",'(//div[@class="c-single-info c-single-info--offer"]//p[@class="c-single-info__price"])[1]/text()')
        item.add_xpath("metros_2",'//div[@class="mt-3 mb-d"]//p[@class="c-single-info__size"]/text()')
        item.add_xpath("descripcion",'//section[@class="c-single-description "]//div//div//*/text()')
        item.add_xpath("direccion",'(//section[@class="c-single-features "]//div//div//ul/li)[1]/text()')

        yield item.load_item()
