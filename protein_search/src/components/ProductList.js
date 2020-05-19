import React, { Component } from 'react';
import Product from '../components/Product';



class ProductList extends Component{
    constructor (props) {
        super(props)
        this.state = {
            "filtered" : [],
        }
      }

      render() {
          console.log("List rendered")
          if(this.props.optionSelected != null){
            if(this.props.optionSelected == "price"){
                  const products = this.props.filtered_products.map((p) => <Product key={p.name} name={p.name} price={p.price} discount={p.discount} description={p.description} price_per_bar={p.price_per_bar} image_url={p.image_url} num_bars={p.num_bars} site_text={p.site_text} lowest_kcal={p.lowest_kcal}/>);
                  return <div className="product-list">
                      {products}
                  </div>
            }
            else if (this.props.optionSelected == "discount"){
                const products = this.props.filtered_products.map((p) => <Product key={p.name} name={p.name} price={p.price} discount={p.discount} description={p.description} price_per_bar={p.price_per_bar} image_url={p.image_url} num_bars={p.num_bars} site_text={p.site_text} lowest_kcal={p.lowest_kcal} />);
                  return <div className="product-list">
                      {products}
                  </div>
            }
            else if (this.props.optionSelected == "amount"){
                const products = this.props.filtered_products.map((p) => <Product key={p.name} name={p.name} price={p.price} discount={p.discount} description={p.description} price_per_bar={p.price_per_bar} image_url={p.image_url} num_bars={p.num_bars} site_text={p.site_text} lowest_kcal={p.lowest_kcal}/>);
                  return <div className="product-list">
                      {products}
                  </div>
            }
            else if (this.props.optionSelected == "kcal"){
                const products = this.props.filtered_products.map((p) => <Product key={p.name} kcal_search={true} name={p.name} price={p.price} discount={p.discount} description={p.description} price_per_bar={p.price_per_bar} image_url={p.image_url} num_bars={p.num_bars} site_text={p.site_text} lowest_kcal={p.lowest_kcal}/>);
                  return <div className="product-list">
                      {products}
                  </div>
            }
            else if (this.props.optionSelected == "relevance"){
                if(this.props.indexed_scores != null){
                const products = this.props.products.map((p) => <Product key={p.name} name={p.name} price={p.price} discount={p.discount} description={p.description} price_per_bar={p.price_per_bar} image_url={p.image_url} num_bars={p.num_bars} site_text={p.site_text} lowest_kcal={p.lowest_kcal}/>);
                const products_sorted = []
                const products_null = []
                if(this.props.indexed_scores.length != products.length){
                    return <p>Waiting for fetch</p>
                }
                else{
                for(var i = 0; i<this.props.products.length; i++){
                    if(products[this.props.indexed_scores[i][0]].price_per_bar != null){
                        products_sorted.push(products[this.props.indexed_scores[i][0]])
                    }
                    else{
                        products_null.push(products[this.props.indexed_scores[i][0]])
                    }
                }
                
                return <div className="product-list">
                    {products_sorted}
                    {products_null}
                </div>
                }
                }
              else{
                    
                  const products = this.props.products.map((p) => <Product key={p.name} name={p.name} price={p.price} discount={p.discount} description={p.description} price_per_bar={p.price_per_bar} image_url={p.image_url} num_bars={p.num_bars} site_text={p.site_text} lowest_kcal={p.lowest_kcal}/>);
                  return <div className="product-list">
                      {products}
                  </div>
              }
            }
            
            else{
                return <div>
                    <p>How did you find this text? This is not supposed to be visible</p>
                </div>
            }
        
    }
    else{
        return <div>
            <p>no option selected</p>
        </div>
    }
         
}
}

export default ProductList