# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Trf5SpiderItem(scrapy.Item):
    numero_processo = scrapy.Field()
    numero_legado = scrapy.Field()
    data_autuacao = scrapy.Field()
    envolvidos = scrapy.Field()
    relator = scrapy.Field()
    movimentacoes = scrapy.Field()


