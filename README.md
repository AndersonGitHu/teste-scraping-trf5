# Teste de Web Scraping

## Objetivo:

Aplicar a técnica de raspagem de dados (scraping) no ambiente web com o intuito de extrair dados. A técnica de scraping foi feita utilizando o framework scrapy como: números de processo, datas de autuação, envolvidos, relator e movimentações. O site usado foi o do TRF-5 (https://www5.trf5.jus.br/cp/).


## Dados: 
	Número de processo (numero_processo)
    Número legado (numero_legado)
	Data de autuação (data_autuacao)
	Envolvidos (envolvidos)
	Relator (relator)
	Movimentações (movimentacoes)


## Configuração do Ambiente: 
- Versão do Python:
    - Python 3.10
- Comandos usados na configuração:
	- `scrapy startproject trf5_spider`
- Bibliotecas/Ferramentas/Extensões:
	- Scrapy
    - Pymongo
	- xPath Helper
    - Regex
- Comandos de instalação das bibliotecas/extensões:
    - `pip install -r requirements.txt`


## Execução do Projeto:

- Instalar o Python 3
- Configurar ambiente Python
- Rodar o comando: `pip install -r requirements.txt`
- Instalar Mongodb
- Colocar os dados de acesso ao Banco de Dados no arquivo settings.py
- No terminal, colocar um dos tais comandos:
   - `scrapy crawl trf5_spider -a cnpj=cnpj_da_empresa`
	- `scrapy crawl trf5_spider -a numero_processo=número_do_processo` 
- Visualizar dados dos processos por meio do Mongo Compass ou outra ferramenta similar  
	

## Métodos da Spider:
  
- Classe Spider [TRF5Spider(scrapy.Spider)] para navegar na web e coletar dados;
- Método start_requests() para personalizar as requisições feitas pelo Spider, condicionando-a para fazer requisições ou por número de processos ou por número de cnpj; 
- Método extrair_processo() para o processamento das requisições spider realizadas na página de processo, por meio dela serão aplicados os laços de repetições e lógica para puxar os dados da maneira pretendida;
- Método buscar_processo() para iterar todos os processos com callback para o método extrair_processo() para que, ao acessar cada página de processo, os dados sejam extraídos. Também incluso variável para mudar de página assim que todos os processos sejam acessados, e com callback para retornar buscar_processo(), a fim de que haja um laço de repetição para também acessar os processos das próximas páginas.
- Pipeline para enviar os dados extraídos para o banco de dados MongoDB

## Dificuldades encontradas:

- O site inicial de buscas do tribunal não faz requisições na mesma aba, e sim abre uma aba separada com uma mesma url, o que dificulta para entender as requsições feitas. No entanto, ao observar o site na busca por cnpj, foi possível encontrar urls que davam direto para a página do processo e, também, para o resultado da busca do cnpj, o que permitiu acessar facilmente as páginas necessárias para a raspagem de dados
- Os xpath das páginas dos processos eram genéricos demais, o que dificultou encontrar chaves específicas para selecionar as tags de interesse para raspagem
- O site do tribunal ocasionalmente ficava fora do ar, o que dificultou o desenvolvimento da Spider
- Um pouco de dificuldade em conectar ao banco de dados devido a não conhecer profundamente o MongoDB