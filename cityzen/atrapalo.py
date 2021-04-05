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
    precio_ant= Field()
    precio= Field()
    descripcion = Field()
    descripcion2 = Field()
    duracion= Field()
    fechas_evento= Field()
    nota_media= Field()
    num_opiniones= Field()
    categoria= Field()
    subcategoria= Field()
    direccion= Field()
    zzlocalidad= Field()


class Atrapalo(CrawlSpider):
    name = 'atrapalo'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        # 'CLOSESPIDER_ITEMCOUNT': 50
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = [ 'www.atrapalo.com']

    start_urls = ['https://www.atrapalo.com/actividades/madrid/online/']

    download_delay = 1

    rules = (
        # Paginación
        Rule(
            LinkExtractor(
                allow= "p-",
                deny=(r'/actividades/$',r'/madrid/$',)

            ), follow=True
        ),
        # Detalle productos
        Rule(
            LinkExtractor(
                # allow=(r'^https://www.atrapalo.com/actividades/', ),
                # deny=(r'https://www.atrapalo.com/actividades/madrid/',)
                restrict_xpaths = ['//div[@id="resultados_espectaculos"]//div[@class="card-result-container"]//a[contains(@class,"product-name")]'] #limitar el espectro de búsqueda

            ), follow= True, callback="parse_items"
        ),
    )


    def parse_items(self,response):
        item= ItemLoader(Articulo(),response)
        item.add_value("link",response.request.url)
        item.add_xpath("titulo",'//h1[@class="detail-title fn"]/text()')
        item.add_xpath("precio",'//ins[@class="final-price"]/text()')
        item.add_xpath("precio_ant",'//span[@class="old-price show-for-large"]/del/text()')
        item.add_xpath("descripcion",'//div[@class="descCorta relative lim-text-esp"]/div/p/text()')
        item.add_xpath("descripcion2",'//div[@class="descCorta relative lim-text-esp"]')
        item.add_xpath("duracion",'//li[@class="date detail-info-box__list-item--iconed duration"]/p/text()')
        item.add_xpath("fechas_evento",'//li[@class="date detail-info-box__list-item--iconed"]/p/text()')
        item.add_xpath("nota_media",'(//span[@class="opinion-rating"])[1]/text()')
        item.add_xpath("num_opiniones",'(//span[@class="overall__number"])[1]/text()')
        item.add_xpath("categoria",'(//p[@class="bread"]/a)[5]/text()')
        item.add_xpath("subcategoria",'(//p[@class="bread"]/a)[6]/text()')
        item.add_xpath("direccion",'(//li[@class="direction"])[2]/span/text()')
        item.add_xpath("zzlocalidad",'(//p[@class="bread"]/a)[3]/text()')
        #
        # if("Madrid" in str(response.selector.xpath('(//p[@class="bread"]/a)[3]/text()').get())):
        #     yield item.load_item()
        yield item.load_item()
