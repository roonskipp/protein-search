import crochet
crochet.setup()

import json
import time
import sys
sys.path.insert(0, '../')


from flask import Flask, request, Response, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

from protein_scraper.protein_scraper.spiders.GG_spider import GGSpider
from protein_scraper.protein_scraper.spiders.GG_spider_nut import GGSpiderNut


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

crawl_runner = CrawlerRunner()      # requires the Twisted reactor to run
products_list = []              # store quotes
nut_products_list = []              # store quotes
scrape_in_progress = False
scrape_complete = False
nut_scrape_in_progress = False
nut_scrape_complete = False



@app.route('/crawl', methods=['POST'])
#@cross_origin()
def crawl_for_products():
    """
    Scrape for products
    """
    global scrape_in_progress
    global scrape_complete

    if request.method == 'POST':
        
        if not scrape_in_progress:
            scrape_in_progress = True
            global products_list
            # start the crawler and execute a callback when complete
            scrape_with_crochet(products_list)
            return json.dumps({"status": 'SCRAPING'})
        elif scrape_complete:
            return json.dumps(products_list)
        return json.dumps({"status": 'SCRAPE IN PROGRESS'})

@app.route('/crawlnut', methods=['POST'])
#@cross_origin()
def crawl_for_products_nut():
    """
    Scrape for products
    """
    global nut_scrape_in_progress
    global nut_scrape_complete

    if request.method == 'POST':
        
        if not nut_scrape_in_progress:
            nut_scrape_in_progress = True
            global nut_products_list
            # start the crawler and execute a callback when complete
            scrape_with_crochet_nut(nut_products_list)
            return json.dumps({"status": 'SCRAPING'})
        elif nut_scrape_complete:
            return json.dumps(nut_products_list)
        return json.dumps({"status": 'SCRAPE IN PROGRESS'})

@app.route('/results')
def get_results():
    """
    Get the results only if a spider has results
    """
    global scrape_complete
    if scrape_complete:
        return json.dumps(products_list)
    return json.dumps({"status": 'SCRAPE STILL IN PROGRESS'})

@crochet.run_in_reactor
def scrape_with_crochet(_list):
    eventual = crawl_runner.crawl(GGSpider, products_list=_list)
    eventual.addCallback(finished_scrape)

@crochet.run_in_reactor
def scrape_with_crochet_nut(_list):
    eventual = crawl_runner.crawl(GGSpiderNut, nut_products_list=_list)
    eventual.addCallback(finished_nut_scrape)


def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global scrape_complete
    scrape_complete = True

def finished_nut_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global nut_scrape_complete
    nut_scrape_complete = True


if __name__ == '__main__':
    app.run(debug=True) 

