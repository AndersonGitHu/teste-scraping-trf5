import scrapy
import re
from datetime import datetime
import scrapy.responsetypes


class TRF5Spider(scrapy.Spider):
    name= 'trf5_spider'

    custom_settings= {}

    def __init__(self, numero_processo = None, cnpj = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.numero_processo = numero_processo
        self.cnpj = cnpj



    def start_requests(self):
        if self.numero_processo:
            yield scrapy.Request(f'https://cp.trf5.jus.br/processo/{self.numero_processo}', callback=self.extrair_processo)
        elif self.cnpj:
            r = re.compile(r'[\D ]')
            cnpj_limpo = r.sub('', self.cnpj)
            yield scrapy.Request(f'https://cp.trf5.jus.br/processo/cpf/porData/{cnpj_limpo}/0', callback=self.buscar_processo)
    


        
    def extrair_processo(self, response, **kwargs):
        
        base = response.xpath('//body[@class="ff"]')
        numero_processo = base.xpath('substring-after(./p[2]/text(), "PROCESSO Nº ")').get()
        numero_legado = base.xpath('./p[3]/text()').get()

        if numero_legado:
            numero_legado = re.findall('[^()]+', numero_legado)[0]
        
        if not numero_processo:
            numero_processo = numero_legado
        
        data_autuacao = datetime.strptime(re.findall('\d{2}\/\d{2}\/\d{4}', base.xpath('.//tr//div/text()').get())[0], '%d/%m/%Y')               
        
        envolvidos_base = base.xpath('./table[3]//tr[position() < last()]')
        envolvidos = []
        for envolvido in envolvidos_base:
            envolvidos_papel = envolvido.xpath('.//td[1]/text()').get()
            envolvidos_nome = envolvido.xpath('.//td/b/text()').get()
            envolvidos.append({
                'papel': envolvidos_papel,
                'nome': envolvidos_nome
            })
        
        relator = base.xpath('substring-after(./table[3]//tr[last()]//b/text(), ": ")').get()

        movimentacoes_base = base.xpath('.//table[5]/following-sibling::table')
        movimentacoes = []
        for movimento in movimentacoes_base:
            movimentacoes_data = datetime.strptime(re.findall('\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}', movimento.xpath('.//li/a/text()').get())[0], '%d/%m/%Y %H:%M')
            movimentacoes_texto = movimento.xpath('.//tr[2]/td[2]/text()').get()
            movimentacoes.append({
                'data': movimentacoes_data,
                'texto': movimentacoes_texto
            })     
        
        yield {
            'numero_processo': numero_processo,
            'numero_legado': numero_legado,
            'data_autuacao': data_autuacao,
            'envolvidos': envolvidos,
            'relator': relator,
            'movimentacoes': movimentacoes
        }

    
    def buscar_processo(self, response, **kwargs):
        acesso_processos = response.xpath('//table[@class="consulta_resultados"]//td[2]/a/@href').getall()    
        for acesso_processo in acesso_processos:
            url_processo = f'https://cp.trf5.jus.br{acesso_processo}'
            yield response.follow(url_processo, callback=self.extrair_processo)
    

    
        mudar_paginas = response.xpath('//table[@class="consulta_paginas"]//a[text() = ">"]/@href').get()
        if mudar_paginas:
            yield response.follow(mudar_paginas, callback=self.buscar_processo)




    