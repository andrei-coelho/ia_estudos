import scrapy
from util.mysqli import mysqli

class NetshoesSpider(scrapy.Spider):

    name = 'Netshoes'
    allowed_domains = ["netshoes.com.br"]

    start_urls = [
        'https://www.netshoes.com.br/botas',
        'https://www.netshoes.com.br/chinelos',
        'https://www.netshoes.com.br/chuteiras',
        'https://www.netshoes.com.br/sapatenis',
        'https://www.netshoes.com.br/tenis',
    ]

    MAX_LINKS = 2000
    categorias  = ['botas', 'chinelos', 'chuteiras', 'sapatenis', 'tenis']


    def parse(self, response):

        categoria_atual = next((cat for cat in self.categorias if cat in response.url), None)
        
        if categoria_atual is None:
            self.logger.error(f"Categoria não encontrada para URL: {response.url}")
            return

        categoria_count = 0

        produto_links = response.css('.product-list__items.double-columns .card.double-columns.full-image a::attr(href)').getall()

        for link in produto_links:
            if categoria_count >= self.MAX_LINKS:
                break
            yield response.follow(link, self.parse_produto, cb_kwargs={'categoria': categoria_atual})
            categoria_count += 1

        proxima_pagina = response.css('a.pagination__next::attr(href)').get()
        if proxima_pagina and categoria_count < self.MAX_LINKS:
            yield response.follow(proxima_pagina, self.parse)



    def parse_produto(self, response, categoria):
    
        nome = response.css('h1.product-name::text').get()
        avaliacao = response.css('.link__average::text').get()
    
        try:
            avaliacao = float(avaliacao)
        except (ValueError, TypeError):
            avaliacao = 0.00 

        descricao = nome
        db = mysqli.instance()
        cursor = db.cursor()

        if isinstance(avaliacao, float):
            sql = """
                INSERT INTO produtos (nome, urli, avaliacao, descricao, categoria) 
                VALUES (%s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (nome, response.url, avaliacao, descricao, categoria))
                db.commit()
            except Exception as e:
                self.logger.error(f"Erro ao inserir dados no banco: {e}")
                db.rollback() 
        else:
            self.logger.error(f"Avaliação inválida para o produto: {nome}")
        
        cursor.close()  