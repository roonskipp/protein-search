# protein-search

Consists of a flask server that starts a scrapy spider that crawls www.gymgrossisten.no for protein bars.
A react client makes a call to the flask server when it loads, and repeats this call until the data is fethced and displayed in the client.
The client can be used to search for products that are scraped by the scraper.

This project uses Scrapy, React.Js, Flask. 

To start this, first run the flask server, then start the react client. Search for products. If you leave the search blank it will return all products that are fetched.
