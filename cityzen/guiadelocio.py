from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class teatro(Item):
    link = Field()
    titulo = Field()
    precio= Field()
    horario= Field()
    descripcion = Field()
    duracion= Field()
    fechas_evento= Field()
    categoria= Field()
    subcategoria= Field()
    direccion= Field()


class guiadelocio(CrawlSpider):
    name = 'guiadelocio'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 100
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = [ 'guiadelocio.com']

    start_urls = ["https://www.guiadelocio.com/madrid/teatro-y-danza/(accion)/filtro/"]

    download_delay = 1

    rules = (
        # Paginación
        Rule(
            LinkExtractor(
                allow= "(offset)/\d+-dºº"
                # deny=("https://www.guiadelocio.com/madrid/teatro-y-danza/(genero)",)
                # deny=(r'/(genero)/',)

            ), follow=True
        ),
        # Detalle productos
        Rule(
            LinkExtractor(
                # allow=(r'^https://www.atrapalo.com/actividades/', ),
                # deny=(r'https://www.atrapalo.com/actividades/madrid/',)
                # restrict_xpaths = ['//div[@id="maincontent"]']
                restrict_xpaths = ['//div[@class="general-result-page"]//article//div[@class="row-fluid mb10 border-bottom"]//a']

            ), follow= True, callback="parse_items"
        ),
    )

    def parse_items(self,response):
        item= ItemLoader(teatro(),response)
        item.add_value("link",response.request.url)
        item.add_xpath("titulo",'//div[@class="container"]//header//h1//a/text()')
        item.add_xpath("precio",'(//div[@class="div-380"]//ul//li)[7]/text()')
        item.add_xpath("horario",'(//div[@class="div-380"]//ul//li)[6]/text()')
        item.add_xpath("descripcion",'//div[@class="row-fluid sinopsis_text"]/div//p/text()')
        item.add_xpath("duracion",'(//div[@class="div-380"]//ul//li)[11]/text()')
        item.add_xpath("fechas_evento",'(//div[@class="div-380"]//ul//li)[2]/text()')
        item.add_value("categoria",'Teatro')
        item.add_xpath("subcategoria",'(//div[@class="div-380"]//ul//li)[1]/text()')
        item.add_xpath("direccion",'(//div[@class="div-380"]//ul//li)[5]/text()')

        yield item.load_item()
