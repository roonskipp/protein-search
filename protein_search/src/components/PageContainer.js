import React, { Component } from 'react'

import SearchBar from '../components/SearchBar';
import ProductList from '../components/ProductList';

import data from '../data.json';


class PageContainer extends Component{
    constructor (props) {
        super(props)
        this.state = {
            products : data,
            filtered : []
        }
      }

      searchProducts = (search) => {

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
        this.setState({
            filtered : relevant_products
        })
        console.log(relevant_products)
      }

      componentDidMount = () => {
        
        console.log(this.state)

      }

      SearchBarCallback = (search) => {
        this.searchProducts(search);
      }

      render() {
          return <div className="page-container">
              <SearchBar SearchCallback={this.SearchBarCallback}/>
              <ProductList products={this.state.filtered}/>
 
          </div>
      }
}

export default PageContainer