import math
import re
import scrapy
from bs4 import BeautifulSoup


class GGSpider(scrapy.Spider):

    # CODES
    GG_CODE = 1000000


    # URLS
    GG_URL = 'https://www.gymgrossisten.no/kosttilskudd/barer'
    GG_BASE_URL = 'https://www.gymgrossisten.no'

    name = "GG"

    start_urls = [
            'https://www.gymgrossisten.no/kosttilskudd/barer'
        ]


    def parse(self, response):

        # check if requested url
        URL_CODE = self.Get_page_code(response.request.url)

        if(URL_CODE == self.GG_CODE):
            ## Gymgrossisten - create custom url
            page_url = self.GG_build_url(self.GG_num_products(response))
            yield scrapy.Request(page_url, callback=self.parse)

        else:
            items = []
            for product in response.xpath('//div[@class="product"]'):

                product_dict = {
                    "name": product.xpath('span[@id="gtm-data"]/@data-name').extract_first(),
                    "price": product.xpath('span[@id="gtm-data"]/@data-price').extract_first(),
                    "discount": product.xpath('.//div[@class="promotion sale"]/span/text()').extract_first()
                }

                price = product.xpath('span[@id="gtm-data"]/@data-price').extract_first()
                if(price == None):
                    price = product.xpath('div[@class="price-sales"]/text()').extract_first().replace('\n', '')
                    product_dict["price"] = price

                product_dict["num_bars"] = self.GG_num_bars(product_dict["name"])
                product_dict["price_per_bar"] = self.PPB(product_dict["num_bars"], product_dict["price"])
                product_dict["image_url"] = "https://www.gymgrossisten.no" + str(product.xpath('.//div/div/div[2]/a/img/@data-src').extract_first())
                
                # Get link from product to product page
                #link = product.xpath('.//a[@class="button product-tile-buy button--small show-for-large"]/@href').extract_first()
                link = product.xpath('.//a/@href').extract_first()
                if(link == None):
                    link = product.xpath('.//div[@class="cart-and-ipay product-tile-add-to-cart show-for-large"]/a/@href').extract_first()
                    if(link == None):
                        link = product.xpath('.//div[@class="product-tile-image__container relative"]/a/@href').extract_first()
                        if(link == None):
                            link = product.xpath('.//div[@class="product-tile-image__container relative"]')
                link = self.GG_build_product_url(link)
                request = scrapy.Request(link, callback = self.parse_product)
                request.meta["product_dict"] = product_dict
                yield request


    def parse_product(self, response):
        description = response.selector.xpath('//div[@class="product-short-description"]/text()').extract_first().strip()
        product_dict = response.meta["product_dict"]
        product_dict["description"] = description

        # add all site text to product dict

        html = response.body.decode("utf-8")
        soup = BeautifulSoup(html)
        html_text = soup.get_text().strip()
        product_dict["site_text"] = html_text

        ## get product label

        # vvvv  uncomment to run for nutrition tables


        # nutrition_tables = response.selector.xpath('//div[@class="master-product-nutrition-and-ingredients"]/div/div[@class="collapsible-content"]/table')
        # can be multiple tables, so have to loop through them


        # might not have found nutrition table as they vary
        # if(nutrition_tables == []):
        #     nutrition_tables = response.selector.xpath('//div[@class="master-product-nutrition-and-ingredients"]/div/div[@class="collapsible-content"]/table')
        #     if(nutrition_tables == []):
        #         nutrition_tables = response.selector.xpath('//div[@class="nutrition-and-ingredients columns"]/table')
        #         if(nutrition_tables == []):
        #             nutrition_tables = response.selector.xpath('//div[@class="nutrition-and-ingredients columns"]')
        #             if(nutrition_tables == []):
        #                 nutrition_tables = response.selector.xpath('//div[@class="long-description columns"]/table')
        #                 if(nutrition_tables == []):
        #                     nutrition_tables = response.selector.xpath('//div[@class="nutrition-and-ingredients columns"]')
        #                     if(nutrition_tables == []):
        #                         print(response.url)
        #                         print("STILL NULL SMORC")
        #                         # swebar wont work




        # print("NUT:", response.selector.xpath('//div[@class="master-product-nutrition-and-ingredients"]/div/div[@class="collapsible-content"]'))
        # sub_products = self.parse_table(nutrition_tables, response.url)
        # product_dict["subproducts"] = sub_products

        # ^^^
        if(product_dict["price"] == "null"):
            return
        self.products_list.append(product_dict)
        yield product_dict

        
    # finds product label information from table
    def parse_table(self, table_object, url):
        # print("PARSE_TABLE - table_object:", table_object)

        # product_index has keys from products list
        # output from product_index[product-name] = column-indices for that product
        index2product = {}
        productDict = {}
        indexTo100g = {}

        # check if there is more than one table_object

        # get all tables from parent node
        all_tables = table_object.xpath('..//table[@class="table table-striped"]')
        all_tables2 = table_object.xpath('..//table[@border="1"]')
        if(len(table_object)>0):
            all_tables3 = table_object[0].xpath('..//table[@class="Table"]')
            if(len(all_tables3) >0):
                # table with class="Table" tables

                # url specific
                if url == "https://www.gymgrossisten.no/12-x-nutramino-proteinbar-60-g-chunky/SETNUTRABAR.html":

                    table_object = table_object.xpath('..//div[@class="master-product-nutrition-and-ingredients"]')
                    # find the nutrition info that is not in a table
                    nut_div = table_object.xpath('.//div/div[2]/p[3]/text()').extract()
                    nut_div_name = table_object.xpath('.//div/div[2]/p[1]/strong/text()').extract_first()
                    

                    tbody = table_object.xpath('.//div/div[2]/div/table/tbody')
                    tbody_name = table_object.xpath('.//div/div[2]/p[4]/text()').extract_first()

                    productDict[nut_div_name] = {
                        "name" : nut_div_name
                    }
                    
                    productDict[tbody_name] = {
                        "name" : tbody_name
                    }

                    for r, row in enumerate(nut_div):
                        row = row.replace('\r\n', '')
                        row = row.split(':')
                        productDict[nut_div_name][row[0]] = row[1]

                    rows = tbody.xpath('.//tr')
                    for r, row in enumerate(rows):
                        if r == 0:
                            continue
                        else:
                            label = row.xpath('.//td/span/span/span/span/span/span/span/span/text()').extract_first()
                            val = row.xpath('.//td/span/span/span/span/span/span/span/text()').extract_first()
                            productDict[tbody_name][label] = val
                            if(label == None):
                                label = row.xpath('.//td/span/span/span/span/span/span/span/text()').extract_first()
                                val = row.xpath('.//td/span/span/span/span/span/span/span/text()').extract()[1]
                                if(label == None):
                                    continue
                                productDict[tbody_name][label] = val
                                break
                                

                    return productDict

                
                #find product names
                strong_texts = table_object[0].xpath('../p/span/span/strong/text()').extract()
                if(len(strong_texts) < len(all_tables3)):
                    missing_product_name = table_object[0].xpath('../p/span/span/text()').extract_first()
                    strong_texts.insert(0, missing_product_name)

                for i, table in enumerate(all_tables3):
                    tbody = table.xpath('.//tbody')
                    productDict[strong_texts[i]] = {
                        "name" : strong_texts[i]
                    }
                    for tr in tbody.xpath('.//tr'):
                        td_list = tr.xpath('.//td/p/span/span/b/span/text()').extract()
                        td_list.append(tr.xpath('.//td/p/span/span/span/text()').extract_first())
                        if td_list == [None]:
                            continue
                        productDict[strong_texts[i]][td_list[0]] = td_list[1]
                print("exit 4")
                print(url)
                return productDict
        if(len(all_tables2) > 0):
            # check for nutra-go-protein-wafer table

            nutra_tables = table_object[0].xpath('../table[@cellpadding="3"]')
            if len(nutra_tables) > 0:
                

                # get names
                product_names = table_object.xpath('../p/strong/text()').extract()[:len(nutra_tables)]
                for n, name in enumerate(product_names):
                    index2product[n] = name
                    productDict[name] = {
                        "name" : name
                    }

                for i, table in enumerate(nutra_tables):
                    rows = table.xpath('.//tr')
                    for j, row in enumerate(rows):
                        columns = row.xpath('.//td/text()').extract()
                        num_entries = len(columns)
                        if num_entries == 3:
                            productDict[index2product[i]][columns[0]] = columns[1]
                        elif num_entries > 3:
                            rows_needed = int((num_entries/3)*2)
                            columns_filtered = columns[:rows_needed]
                            for x in range(1, int(rows_needed/2)):
                                productDict[index2product[i]][columns_filtered[x]] = columns_filtered[x+int(rows_needed/2)]
                print("exit 3")
                print(url)
                return productDict



            else:
                
                # specific case
                if url == "https://www.gymgrossisten.no/12-x-propud-protein-bar-55-g/SETPROPUDBAR.html":
                    for t, table in enumerate(all_tables2):
                        name = ""
                        tbody = table.xpath('.//tbody')
                        rows = tbody.xpath('.//tr')
                        for r, row in enumerate(rows):
                            cols = row.xpath('.//td')
                            if r == 0:
                                cols_text = cols.xpath('.//text()').extract()
                                name = cols_text[0]
                                name = name.replace('Næringsinnhold ', '')
                                index2product[t] = name
                                productDict[name] = {
                                    "name" : name
                                }
                            else:
                                cols_text = cols.xpath('.//text()').extract()
                                productDict[index2product[t]][cols_text[0]] = cols_text[1]
                    print("exit 6")
                    print(url)
                    return productDict

                else:
                    # specific url case
                    if(url == "https://www.gymgrossisten.no/goodlife-50-g/6519R.html"):
                        for t, table in enumerate(all_tables2):
                            name = ""
                            tbody = table.xpath('.//tbody')
                            rows = tbody.xpath('.//tr')
                            for r, row in enumerate(rows):
                                cols = row.xpath('.//td')
                                if r == 0:
                                    cols_text = cols.xpath('.//strong/text()').extract()
                                    # clean this text, it has br and \t

                                    clean_cols = []
                                    for col in cols_text:
                                        clean_cols.append(col.replace("\t", ''))
                                    cols_text = clean_cols

                                    # concatenate
                                    conc_cols = []
                                    for x , col in enumerate(cols_text):
                                        if x % 2 == 0:
                                            conc_cols.append(cols_text[x]+" "+cols_text[x+1])
                                    cols_text = conc_cols

                                    for c, col in enumerate(cols_text):
                                        if c == 0:
                                            continue
                                        else:
                                            index2product[c] = col
                                            productDict[col] = {
                                                "name" : col
                                            }
                                else:
                                    cols_text = []
                                    for col in cols:
                                        col_text = col.xpath('.//text()')
                                        if(len(col_text) > 1):
                                            
                                            data = col.xpath('.//text()').extract()
                                            data = ' '.join(data)
                                            data = data.replace('\t', '')
                                            cols_text.append(data)
                                        else:
                                            cols_text.append(col.xpath('.//text()').extract_first().replace('\t', ''))

                                    row_label = cols_text[0]
                                    for c, col in enumerate(cols_text):
                                        if c == 0:
                                            continue
                                        else:
                                            productDict[index2product[c]][row_label] = col
                        print("exit 7")
                        return productDict
                    
                    # specific url case
                    if url == "https://www.gymgrossisten.no/12-x-goodlife-deluxe-60-g/SETGDLUX.html" or url =="https://www.gymgrossisten.no/goodlife-deluxe-60-g/6565R.html":
                        for table in all_tables2:
                            tbody = table.xpath('.//tbody')
                            rows = tbody.xpath('.//tr')
                            for i, row in enumerate(rows):
                                if i == 0:
                                    cols = row.xpath('.//td/p/strong/text()').extract()
                                    for c, col in enumerate(cols):
                                        if c % 2 == 1:
                                            index2product[c] = col
                                            productDict[col] = {
                                                "name" : col
                                            }
                                elif i == 1:
                                    continue
                                else:
                                    cols = row.xpath('.//td/p/text()').extract()
                                    for c, col in enumerate(cols):
                                        row_label = cols[0]
                                        if c == 0:
                                            continue
                                        elif c in index2product.keys():
                                            productDict[index2product[c]][row_label] = col
                        print("exit 8")
                        return productDict
                                        
                    #specific url case

                    if url == "https://www.gymgrossisten.no/star-nutrition-protein-bar-55g/887R.html" or url == "https://www.gymgrossisten.no/12-x-star-nutrition-protein-bar-55g/SETSTAPR.html":
                        for table in all_tables2:
                            tbody = table.xpath('.//tbody')
                            rows = table.xpath('.//tr')
                            for i, row in enumerate(rows):
                                if i == 0:
                                    cols = row.xpath('.//td/p/strong/text()').extract()
                                    for j, col in enumerate(cols):
                                        if j == 0:
                                            continue
                                        else:
                                            if j % 2 == 1:
                                                index2product[j] = col
                                                productDict[col] = {
                                                    "name" : col
                                                }
                                if i == 1:
                                    continue
                                else:
                                    cols = row.xpath('.//td/p/text()').extract()
                                    if len(cols) < 1:
                                        continue
                                    row_label = cols[0]
                                    for j, col in enumerate(cols):
                                        if j in index2product.keys():
                                            productDict[index2product[j]][row_label] = col
                        print("exit 10")
                        return productDict
                    
                    # specific url case
                    elif url == "https://www.gymgrossisten.no/barebells-protein-bar-55-g/9789-004R.html":
                        for t, table in enumerate(table_object):
                            # get name
                            x = str(1+ t*2)
                            name1 = table.xpath('..//div[1]/strong/text()').extract_first()
                            name2 = table.xpath('..//div[7]/b/text()').extract_first()
                            name3 = table.xpath('..//div[11]/strong/text()').extract_first()
                            names = [name1, name2, name3]
                            for i, name in enumerate(names):
                                index2product[i] = name
                                productDict[name] = {
                                    "name" : name
                                }
                            
                        for t, table in enumerate(table_object):
                            tbody = table.xpath('.//tbody')
                            rows = tbody.xpath('.//tr')
                            for r, row in enumerate(rows):
                                if r == 0:
                                    continue
                                else:
                                    cols = row.xpath('.//td/div/text()').extract()
                                    if len(cols) <1:
                                        continue
                                    productDict[index2product[t]][cols[0].replace('\t', '')] = cols[1].replace('\t', '')
                        print("exit 11")
                        return productDict

                    # specific url
                    if url == "https://www.gymgrossisten.no/12-x-vegan-protein-bar-50-g/SETVEGBAR.html" or url == "https://www.gymgrossisten.no/vegan-protein-bar-50-g/8637R.html":

                        table_object = table_object[0]

                        tbody = table_object.xpath('.//tbody')
                        rows = tbody.xpath('.//tr')
                        for r, row in enumerate(rows):
                            if r == 0:
                                cols = row.xpath('.//td/p/strong/text()').extract()
                                for c, col in enumerate(cols):
                                    if c % 2 == 1:
                                        index2product[c] = col
                                        productDict[col] = {
                                            "name" : col
                                        }
                                continue
                            elif r == 1:
                                continue
                            else:
                                label = row.xpath('.//td/p/strong/text()').extract_first()
                                cols = row.xpath('.//td/p/text()').extract()
                                for v, val in enumerate(cols):
                                    if v % 2 == 0:
                                        productDict[index2product[v+1]][label] = val
                        print("exit 13")
                        return productDict

                    if url == "https://www.gymgrossisten.no/12-x-quest-bar-60-g/SA001241.html":
                        table_object = table_object[0].xpath('../../../../../div/div[@class="nutrition-and-ingredients columns"]')

                        tables = table_object.xpath('.//table')

                        for t, table in enumerate(tables):
                            tbody = table.xpath('.//tbody')
                            rows = tbody.xpath('.//tr')
                            for r, row in enumerate(rows):
                                if r == 0 or r == 12 or r == 24 or r == 35 or r == 46 or r == 57 or r == 68 or r == 80 or r == 92 or r==104:
                                    cols = row.xpath('.//td/span/span/span/span/span/span/text()').extract()
                                    for c, col in enumerate(cols):
                                        if c == 0:
                                            continue
                                        else:
                                            index2product[c] = col.strip()
                                            productDict[col.strip()] = {
                                                "name": col.strip()
                                            }
                                else:
                                    cols = row.xpath('.//td/span/span/span/span/span/span/text()').extract()
                                    if len(cols)<1:
                                        continue
                                    label = cols[0]
                                    
                                    for c, col in enumerate(cols):
                                        if c == 0:
                                            continue
                                        else:
                                            productDict[index2product[c]][label.strip()] = col.strip()
                                        


                        print("exit 14")
                        return productDict
                                
                    

                    if url == "https://www.gymgrossisten.no/12-x-best-bar-60-g/SETBESTBAR.html":

                        for table in table_object:
                            tbody = table.xpath('.//tbody')
                            rows = tbody.xpath('.//tr')
                            for r, row in enumerate(rows):
                                if r == 0:
                                    cols = row.xpath('.//td/p/strong/text()').extract()
                                    for c, col in enumerate(cols):
                                        if c == 0:
                                            continue
                                        else:
                                            if c % 2 == 0:
                                                index2product[c] = col
                                                productDict[col] = {
                                                    "name" : col
                                                }
                                elif r == 1:
                                    continue
                                else:
                                    cols = row.xpath('.//td/p/text()').extract()
                                    label = cols[0]
                                    for c, col in enumerate(cols):
                                        if c == 0:
                                            continue
                                        else:
                                            if c in index2product.keys():
                                                productDict[index2product[c]][label] = col
                        print("exit 15")
                        return productDict

                    if url == "https://www.gymgrossisten.no/20-x-swebar-55-g/SET000217.html":
                        print("yoink")
                        print("TABLE_OBJECT:", table_object)
                        print("exit 16")
                        return productDict

                    for table in all_tables2:
                        tbody = table.xpath('.//tbody')
                        tr_list = tbody.xpath('.//tr')
                        column2product = {}
                        for i, tr in enumerate(tr_list):
                            text = tr.xpath('.//text()').extract()

                            # remove whitespace
                            no_ws_text = []
                            for entry in text:
                                if not entry.isspace():
                                    no_ws_text.append(entry)
                            text = no_ws_text
                            if i == 0:
                                # top of table, get product names
                                for j, entry in enumerate(text):
                                    entry.replace('\t', '')
                                    if j == 0:
                                        continue # this column says "Smak"
                                    else:
                                        index2product[j] = entry
                                        productDict[entry] = {
                                            "name" : entry
                                        }
                            elif i == 1:
                                # we are on second row here is the nutriton per/100g per /50g labels
                                num_columns = len(text)
                                num_products = len(index2product.keys())
                                
                                running_substraction = 0
                                for k, column in enumerate(text):
                                    if k == 0:
                                        continue
                                    else:
                                        if k%2 == 1:
                                            # we have a 100g
                                            productNumber = k - running_substraction
                                            running_substraction += 1
                                            column2product[k] = index2product[productNumber]
                            else:
                                label = text[0].replace('\t', '')
                                for e, entry in enumerate(text):
                                    entry = entry.replace('\t', '')
                                    if e == 0:
                                        continue
                                    else:
                                        if e not in column2product.keys():
                                            continue
                                        else:
                                            productDict[column2product[e]][label] = entry
                    print("exit 2")
                    print(url)
                    return productDict



        if len(all_tables) > 0:
            product_names = table_object.xpath('..//p/span/strong/text()').extract()

            tbodies = table_object.xpath('..//table/tbody')

            for i, body in enumerate(tbodies):
                # i = index of table and thus product name in product_names
                tr_list = body.xpath('.//tr')
                index2product[i] = product_names[i]
                productDict[product_names[i]] = {
                    "name" : product_names[i].replace('\t', '')
                }

                for j, tr in enumerate(tr_list):
                    # th = description column, left
                    # td = value column, right
                    th = tr.xpath('.//th/text()').extract_first()
                    if(th == None):
                        td = tr.xpath('.//td/text()').extract()
                        productDict[product_names[i]][td[0]] = td[1]
                    else:
                        td = tr.xpath('.//td/text()').extract_first()
                        productDict[product_names[i]][th] = td
            print("exit 1")
            print(url)
            return productDict
        
        else:
            
            if url == "https://www.gymgrossisten.no/16-x-nutramino-xl-proteinbar-82-g/SETNUTRAMINO8.html":
                table_object = table_object[0]
                tbody = table_object.xpath('.//tbody')
                productDict["XL bar"] = {
                    "name" : "XL bar"
                }
                rows = tbody.xpath('.//tr')
                for r, row in enumerate(rows):
                    cols = row.xpath('.//td/div/text()').extract()
                    productDict["XL bar"][cols[0].replace('\t', '')] = cols[1].replace('\t', '')
                print("exit 12")
                return productDict

            # specific url case
            if url == "https://www.gymgrossisten.no/rox-protein-bar-55-g/100590580020-1R.html" or url == "https://www.gymgrossisten.no/15-x-rox-protein-bar-55-g/SETROXBAR.html":
                t_body = table_object.xpath('.//tbody')
                rows = t_body.xpath('.//tr')
                productDict["ROX"] = {
                    "name" : "ROX bar unknown flavor"
                }
                for i, row in enumerate(rows):
                    cols = row.xpath('.//td/text()').extract()
                    if i == 0:
                        continue
                    else:
                        productDict["ROX"][cols[0]] = cols[1]

                print("exit 9")
                return productDict
        
            t_body = table_object.xpath('.//tbody')
            # check if table has caption
            table_caption = table_object.xpath('.//caption/text()').extract_first()

            tr_list = t_body.xpath('.//tr')


            if (len(tr_list) == 0):
                print("FALSE")


                # check for goodlife table

                return False



            for i, tr in enumerate(tr_list):

                # list of columns in current row
                td_list = tr.xpath('.//td')
                p_list = td_list.xpath('.//p')
                
                if(len(p_list) == 0):
                    # different style table, look for divs
                    p_list = td_list.xpath('.//div')
                    if(len(p_list) == 0):
                        # different style table, look for text in td
                        p_list = td_list.xpath('text()')
                        if(len(p_list) == 0):
                            # different style table
                            pass



                # text = list ['column0 text', 'column1 text', 'column2 text' ...]
                text = p_list.xpath('.//text()').extract()

                if(i==0):
                    # Create product

                    for j, text_entry in enumerate(text):
                        if j == 0:
                            # skip row-label
                            continue
                        else:
                            # if text is not in index2product dict, add it
                            if text_entry not in index2product.keys():
                                index2product[j] = text_entry
                                productDict[text_entry] = {
                                    "name" : text_entry,
                                }

                elif(i==1):
                    # Nutrition label "/100g /60g etc"
                    regex_text = re.search("per\s100\sg", str(text))
                    if regex_text != None:
                        filtered_text = regex_text[0]
                        for j, text_entry in enumerate(text):
                            if j == 0:
                                # skip row-label
                                continue
                            elif filtered_text == "per 100 g":
                                # j = the index of product [j] 100g nutrition info
                                cur_prod_name = index2product[j]
                                indexTo100g[j] = cur_prod_name

                        
                # "regular row" - index 0 = row key/label
                else:
                    if text == []:
                        continue
                    row_label = text[0]
                    for j, text_entry in enumerate(text):
                        if j == 0:
                            continue
                        else:
                            if j in indexTo100g.keys():

                                cur_prod_name = indexTo100g[j]
                                productDict[cur_prod_name][row_label] = text_entry
                            else:
                                continue
                    
            # At this point productDict should have all products with information
            print("exit 0")
            print(url)
            return productDict





    # finds amount of products on the page, returns it based on loading 36 new products at a time
    # After testing, it is not needed to find ceil * 36, can just feed it amount of products.
    def GG_num_products(self, response):
        num_products = response.xpath('//div[@class="grid-footer"]//@data-product-count').extract_first()
        return math.ceil(int(num_products) / 36)*36


    # Gets page for bars based on the load-more button
    def GG_build_url(self, num_products):
        url_pt1 = "https://www.gymgrossisten.no/kosttilskudd/barer?sz="
        url_pt2 = "&start=0"
        return url_pt1 + str(num_products) + url_pt2


    # Not needed if doing separate spiders, unless expanding for more products than only bars
    def Get_page_code(self, request_url):
        if request_url == self.GG_URL:
            return self.GG_CODE


    # Takes in title, returns amount of bars
    def GG_num_bars(self, title):
        
        num_bars = re.search("\d+\sx{1}", str(title))
        if num_bars != None:
            num_bars = num_bars[0][0:-2]
        elif num_bars == None:
            num_bars = re.search("\d+\sbar", str(title))
            if num_bars != None:
                num_bars = num_bars[0][0:-4]
            elif num_bars == None:
                num_bars = re.search("x\s\d+", str(title))
                if num_bars != None:
                    num_bars = num_bars[0][2:]
                else:
                    num_bars = str(1)
        
        return num_bars
    
    # get price per bar
    def PPB(self, num_bars, price):
        if num_bars == "null":
            return None
        elif price == "null":
            return None
        elif num_bars != None and price != None:
            return str(float(price)/ float(num_bars))[0:5]

    # get url for product
    def GG_build_product_url(self, url):
        return self.GG_BASE_URL + str(url)
