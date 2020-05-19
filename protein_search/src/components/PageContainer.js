import React, { Component } from 'react'

import Loader from 'react-loader-spinner'

import SearchBar from '../components/SearchBar';
import ProductList from '../components/ProductList';
import RadioButtons from '../components/RadioButtons';
import NutritionSwitch from '../components/NutritionSwitch';



// import data from '../data.json';


class PageContainer extends Component{
    constructor (props) {
        super(props)
        this.state = {
            products : null,
            filtered : [],
            scraping: true,
            optionSelected: null,
            documents: null,
            word2id: null,
            id2word: null,
            document_vectors : null,
            maxlen : null,
            search_vec : null,
            cosine_products : null,
            search_string : "",
            crawl_endpoint : "crawl",
            checked : false
        }
      }

      buildSearchVector = (search) => {
        let search_string = search.toLowerCase()
        search_string = search_string.split(' ')
        let searchVec =  Array(this.state.maxlen).fill(0)
        for(var i=0; i< search_string.length; i++){
          let word = search_string[i];
          if(Object.keys(this.state.word2id).includes(word)){
            searchVec[this.state.word2id[word]] = 1;
          }
        }
        this.setState({
          search_vec : searchVec
        }, () => this.cosineSim())
      }

      cosineSim = () => {
          let cosine_scores = {}
          let indexed_scores = []
          for( var i = 0; i<this.state.document_vectors.length; i++){
            let doc_vec = this.state.document_vectors[i];
            let doc_vec_mag = Math.sqrt(doc_vec.reduce((a, b) => a + b, 0));
            let search_vec_mag = Math.sqrt(this.state.search_vec.reduce((a, b) => a +b, 0));
            let bottom = doc_vec_mag * search_vec_mag
            let dot_product = 0
            // get top which should be dot product of doc_vec and search_vec
            for(var j=0; j<this.state.maxlen; j++){
                dot_product += (doc_vec[j] * this.state.search_vec[j])
            }
            cosine_scores[i] = (dot_product/bottom)
            indexed_scores.push([i, (dot_product/bottom)])
          }
          indexed_scores.sort(function(first, second) {
            return second[1] - first[1];
          });
            this.setState({
              cosine_products : indexed_scores
            })

      }

      buildDocs = () => {
        console.log("build docs")
        let site_texts = []
        for(var i = 0; i< this.state.products.length; i++){
          site_texts.push(this.state.products[i].site_text)
        }
        this.setState({
          documents : site_texts
        }, () => this.buildTermDict())
      }

      buildTermDict = () => {
        let vocab = []
        let maxlen = 0
        let documents = this.state.documents;
        let updated_docs = []
        for(var i=0; i<documents.length; i++){
            let doc = documents[i];
            doc = doc.replace(/(\r\n|\n|\r)/gm, " ");
            doc = doc.replace(/ +(?= )/g,'');
            doc = doc.toLowerCase()
            doc = doc.split(" ");
            updated_docs.push(doc)
            if(doc.length > maxlen){
              maxlen = doc.length
            }
            for(var j=0; j<doc.length; j++){
              let word = doc[j];
              if (!vocab.includes(word)){
                vocab.push(word)
              }
            }
        }
        this.setState({
          documents : updated_docs
      }, () => this.buildWord2Id(vocab))
      }

      buildWord2Id = (vocab, maxlen) => {
        let word2id = {}
        let id2word = {}
        for(var i = 0; i< vocab.length; i++){
          let word = vocab[i]
          word2id[word] = i
          id2word[i] = word
        }
        this.setState({
          word2id: word2id,
          id2word: id2word,
          maxlen : Object.keys(word2id).length
        }, () => this.buildVectors(word2id, id2word))

      }

      buildVectors = (word2id, id2word) => {
        let documents = this.state.documents
        let document_vectors = []
        let maxlen = Object.keys(word2id).length
        let old_doc = []
        for(var i = 0; i<documents.length; i++){
          let docVec =  Array(maxlen).fill(0)
          let doc = documents[i]
          for(var j=0; j<doc.length; j++){
            let word = doc[j]
            docVec[word2id[word]] = 1
          }
          document_vectors.push(docVec)
        }
        this.setState({
          document_vectors : document_vectors
        }, () => this.searchProducts(this.state.search_string))
      }

     
      handleOptionChange = (optionSelected) =>{
        this.setState({
          optionSelected : optionSelected
        }, () => {
          
          this.searchProducts("")
        })
      }

      searchProducts = (search) => {
        if (this.state.products == null){
          return
        }
        

        // get searchstring
        var searchString = search
        var relevant_products = []

        if(searchString != null){
            // loop through all products
            for(var i=0; i<this.state.products.length; i++){
                var product = this.state.products[i]
                if(product.description.toLowerCase().includes(searchString.toLowerCase()) | product.name.toLowerCase().includes(searchString.toLowerCase())){
                    relevant_products.push(product)
                }
            }
        }
        if(this.state.optionSelected == "price"){
          relevant_products.sort((a,b) => (a.price_per_bar < b.price_per_bar) ? -1 : 1)
          this.setState({
            filtered : relevant_products
          })
        }
        else if (this.state.optionSelected == "discount"){
          relevant_products.sort((a,b) => (a.discount > b.discount) ? -1 : 1)
          this.setState({
            filtered : relevant_products
          })
        }
        else if (this.state.optionSelected == "kcal"){
          relevant_products.sort((a,b) => (a.lowest_kcal < b.lowest_kcal) ? -1 : 1)
          console.log(relevant_products)
          this.setState({
            filtered : relevant_products
          })
        }
        else if (this.state.optionSelected == "amount"){
          relevant_products.sort((a,b) => (a.num_bars > b.num_bars) ? -1 : 1)
          this.setState({
            filtered : relevant_products
          })
        }
        else if(this.state.optionSelected == "relevance"){
          console.log("debug ")
         this.buildSearchVector(this.state.search_string)
        }
        else{
        this.setState({
            filtered : relevant_products
        }, () => this.buildSearchVector(search))
        }
      }

      componentDidMount = () => {
        
        this.CallCrawler()
      }

      handleSwitchChange = (checked) => {
        if(checked == true){
          this.setState({
            crawl_endpoint : "crawlnut",
            checked : true
          }, () => this.CallCrawler())
        }
        else{
          this.setState({
            crawl_endpoint : "crawl",
            checked: false
          }, () => this.CallCrawler())
        }
      }

      SearchBarCallback = (search) => {
        this.setState({
          search_string : search
        }, () => this.searchProducts(search))
      }

      CallCrawler = async () => {
        this.setState({
          scraping: true
        })
        
        let crawlAgain = false;

          let options = {headers: {'Content-Type': 'application/json'},
            
          method: 'POST',
          mode: 'cors',
          
        };
      
        await fetch('http://localhost:5000/' + this.state.crawl_endpoint, options)
          .then(async response => 
            response.json())
            .then(data => {
              if (data.hasOwnProperty('status')){
                  crawlAgain = true
              }
              else {
                this.setState({
                  products: data,
                  scraping: false
                }, () => this.buildDocs())

              }
            })
          

          .catch(error => console.error(error))

        if(crawlAgain){
          await this.sleep(2000);
          console.log("Calling server again...")
          this.CallCrawler()
        }
        }
        
        sleep= (ms) => {
          return new Promise(resolve => setTimeout(resolve, ms));
        }

      render() {
        if (this.state.scraping){

          return <div className="page-container">
            <p>Waiting for scraping to finish</p>
            <Loader  type="Puff"
         color="#00BFFF"
         height={100}
         width={100}/>
      </div>
        }
        else{
          console.log("STATE")
          console.log(this.state)
          return <div className="page-container">
              <NutritionSwitch checked={this.state.checked} handleSwitchChange={this.handleSwitchChange}/>
              <SearchBar SearchCallback={this.SearchBarCallback}/>
              <RadioButtons optionSelected={this.state.optionSelected} handleOptionChange={this.handleOptionChange}/>
              <ProductList optionSelected={this.state.optionSelected} products={this.state.products} filtered_products={this.state.filtered} indexed_scores={this.state.cosine_products}/>
          </div>
        }
      }
}

export default PageContainer