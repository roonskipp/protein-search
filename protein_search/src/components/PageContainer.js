import React, { Component } from 'react'

import Loader from 'react-loader-spinner'

import SearchBar from '../components/SearchBar';
import ProductList from '../components/ProductList';
import RadioButtons from '../components/RadioButtons';



// import data from '../data.json';


class PageContainer extends Component{
    constructor (props) {
        super(props)
        this.state = {
            products : null,
            filtered : [],
            scraping: true,
            optionSelected: null
        }
      }

     
      handleOptionChange = (optionSelected) =>{
        console.log(optionSelected);
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
        else if (this.state.optionSelected == "amount"){
          relevant_products.sort((a,b) => (a.num_bars > b.num_bars) ? -1 : 1)
          this.setState({
            filtered : relevant_products
          })
        }
        else{
        this.setState({
            filtered : relevant_products
        })
        }
      }

      componentDidMount = () => {
        
        console.log(this.state)
        this.CallCrawler()

      }

      SearchBarCallback = (search) => {
        this.searchProducts(search);
      }

      CallCrawler = async () => {
        
        let crawlAgain = false;

          let options = {headers: {'Content-Type': 'application/json'},
            
          method: 'POST',
          mode: 'cors',
          
        };
      
        await fetch('http://localhost:5000/crawl', options)
          .then(async response => 
            response.json())
            .then(data => {
              if (data.hasOwnProperty('status')){
                  console.log(data);
                  crawlAgain = true
              }
              else {
                console.log(data);
                console.log("Setting state")
                this.setState({
                  products: data,
                  scraping: false
                })

              }
            })
          

          .catch(error => console.error(error))

        if(crawlAgain){
          await this.sleep(2000);
          console.log("LOL")
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
          return <div className="page-container">
              <SearchBar SearchCallback={this.SearchBarCallback}/>
              <RadioButtons handleOptionChange={this.handleOptionChange}/>
              <ProductList products={this.state.filtered}/>
          </div>
        }
      }
}

export default PageContainer