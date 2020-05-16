import React, { Component } from 'react';
import Product from '../components/Product';



class ProductList extends Component{
    constructor (props) {
        super(props)
        this.state = {
            "filtered" : []
        }
      }

      render() {
            const products = this.props.products.map((p) => <Product key={p.name} name={p.name} price={p.price} discount={p.discount} description={p.description} price_per_bar={p.price_per_bar} image_url={p.image_url} num_bars={p.num_bars}/>);
            console.log(products)
            return <div className="product-list">
                {products}
            </div>
          }
}

export default ProductList