# scraping du site https://download.geofabrik.de/ 
# commencer par accèder à la page https://download.geofabrik.de/europe.html 
# puis cliquer sur le lien France https://download.geofabrik.de/europe/france.html
# puis https://download.geofabrik.de/europe/france/nord-pas-de-calais.html
# extraire les liens des fichiers .osm.pbf 
# puis chercher la balise /html/body/div[4]/div[1]/ul[1]/li[1] sous forme de texte

import scrapy
from scrapy.http import Response
from scrapy.selector import Selector
from pbfcrwal.items import PbfcrwalItem 


class PbfNordPasDeCalaisSpider(scrapy.Spider):
    name = 'pbf_nord_pas_de_calais'
    allowed_domains = ['download.geofabrik.de']
    start_urls = ['https://download.geofabrik.de/europe/france/nord-pas-de-calais.html']

    def parse(self, response: Response):
        """
        Parse les réponse de la page pour extraire les liens des fichiers .osm.pbf
        et les métadonnées associées.
        :param response: La réponse de la requête HTTP
        :return: Un item contenant les métadonnées et le lien vers le fichier .osm.pbf
        """
        item = PbfcrwalItem()
        # parser le texte spécifique de la balise pour récupérer les métadonnées
        specific_text = response.xpath('/html/body/div[4]/div[1]/ul[1]/li[1]/text()').get()
        item['text'] = specific_text.strip()
        # Extraire les liens des fichiers .osm.pbf
        pbf_link = response.css('a[href$=".osm.pbf"]::attr(href)').get()
        item['url'] =  response.urljoin(pbf_link) if pbf_link else None
        yield item