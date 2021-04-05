"""
OBJETIVO:
    - Extraer informacion sobre los hoteles de Guayaquil en TRIPADVISOR.
    - Aprender a realizar extracciones verticales utilizando reglas
    - Aprender a utilizar MapCompose para realizar limpieza de datos
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 14 ABRIL 2020
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

# CLASE CORE - Al querer hacer extraccion de multiples paginas, heredamos de CrawlSpider
class TripAdvisor(CrawlSpider):
    name = 'hotelestripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 5
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['tripadvisor.es']

    # Url semilla a la cual se hara el primer requerimiento
    start_urls = ['https://www.tripadvisor.es/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    download_delay = 2

    # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
    rules = (
        Rule( # Regla de movimiento VERTICAL hacia el detalle de los hoteles
            LinkExtractor(
                allow=r'/Hotel_Review-' # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse_hotel"), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )

    # Funcion a utilizar con MapCompose para realizar limpieza de datos
    def limpiar_precio(self, texto):
        # texto= texto.replace("€", "")
        # precios=texto.split(",")
        # if len(precios)<2:
        #     return(precios)
        # else:
        #     return([int(x) for x in precios])
        return texto
    # Callback de la regla
    def parse_hotel(self, response):
        sel = Selector(response)

        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')

        item.add_xpath('precio','//div[@class="ui_columns is-mobile is-multiline is-vcentered is-gapless-vertical _2mWM5u8t" or @class= "ui_columns is-gapless is-mobile"]//div[contains(text(),"$")]')

        item.add_xpath('descripcion','//div[contains(@data-ssrev-handlers,"load") and contains(@data-ssrev-handlers,"Description")]/div[1]/div[contains(text(),"")]')

        item.add_xpath('amenities','//div[contains(@data-ssrev-handlers,"amenities")]//text()')
        yield item.load_item()

# EJECUCION
# scrapy runspider 1_tripadvisor.py -o tripadvisor.csv -t csv