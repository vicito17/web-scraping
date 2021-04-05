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


class MercadoLibre(CrawlSpider):
    name = 'mercadolibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        # 'CLOSESPIDER_ITEMCOUNT': 10
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = [ 'listado.mercadolibre.com.ec','articulo.mercadolibre.com.ec']

    start_urls = ['https://listado.mercadolibre.com.ec/animales-mascotas/perros/']

    download_delay = 1

    rules = (
        # Paginación
        Rule(
            LinkExtractor(
                allow= "/_Desde_"
            ), follow=True
        ),
        # Detalle productos
        Rule(
            LinkExtractor(
                allow=r'/MEC'
            ), follow= True, callback="parse_items"
        ),
    )
    def limpiar(self, texto):
        nuevotexto=texto.replace("\n","").replace("\t","").replace("\r","")
        return  nuevotexto


    def parse_items(self,response):
        item= ItemLoader(Articulo(),response)
        item.add_value("link",response.request.url)
        item.add_xpath("titulo","//h1/text()", MapCompose(self.limpiar))
        item.add_xpath("descripcion",'//div[@class="item-description__text"]/p/text()', MapCompose(self.limpiar))
        item.add_xpath("precio",'//span[@class="price-tag-fraction"]/text()')


        yield item.load_item()

