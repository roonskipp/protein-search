import React, { Component } from 'react'

class Product extends Component{
    constructor (props) {
        super(props)
        this.state = {
            "name": props.name,
            "price": props.price,
            "discount": props.discount,
            "num_bars": props.num_bars,
            "price_per_bar": props.price_per_bar,
            "image_url": props.image_url,
            "description": props.description,
            "site_text" : props.site_text
          
        }
      }

      render() {
          return <div className="product">
              <p className="product-name">{this.state["name"]}</p>
              <p className="product-price">pris per bar: {this.state["price_per_bar"]},- kr</p>
              <p className="product-price">pris for product: {this.state["price"]},- kr</p>
              <p className="product-discount">rabatt: {this.state["discount"]}</p>
              <p className="product-num_bars">antall barer: {this.state["num_bars"]}</p>
              {/*<p className="product-image-url">{this.state["image_url"]}</p> */}
              <img src={this.state["image_url"]} alt="null"/>
              <p className="product-description">Produktbeskrivelse: {this.state["description"]}</p>
      {/*<p className="product-description">Site-text: {this.state["site_text"]}</p>*/}
          </div>
      }
}

export default Product