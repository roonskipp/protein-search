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
            "site_text" : props.site_text,
            "lowest_kcal" : props.lowest_kcal,
            "kcal_search" : props.kcal_search,
          
        }
      }

      render() {
          if(this.props.kcal_search){
              console.log(this.props.lowest_kcal)
            if(this.props.lowest_kcal == null){
                return<div></div>
            }
            else{
            return <div className="product">
                <p className="product-name">{this.state["name"]}</p>
                <p className="product-price">price per bar: {this.state["price_per_bar"]},- kr</p>
                <p className="product-price">price for product: {this.state["price"]},- kr</p>
                <p className="product-discount">Discount: {this.state["discount"]}%</p>
                <p className="product-num_bars">Amount of bars: {this.state["num_bars"]}</p>
                {/*<p className="product-image-url">{this.state["image_url"]}</p> */}
                <img src={this.state["image_url"]} alt="null"/>
                <p className="product-description">Product description: {this.state["description"]}</p>
                <p className="product-lowest-kcal">lowest_kcal: {this.props.lowest_kcal}</p>
        {/*<p className="product-description">Site-text: {this.state["site_text"]}</p>*/}
            </div>
            }
          }
        else{
            return <div className="product">
            <p className="product-name">{this.state["name"]}</p>
            <p className="product-price">price per bar: {this.state["price_per_bar"]},- kr</p>
            <p className="product-price">price for product: {this.state["price"]},- kr</p>
            <p className="product-discount">Discount: {this.state["discount"]}</p>
            <p className="product-num_bars">Amount of bars: {this.state["num_bars"]}</p>
            {/*<p className="product-image-url">{this.state["image_url"]}</p> */}
            <img src={this.state["image_url"]} alt="null"/>
            <p className="product-description">Product description: {this.state["description"]}</p>
            {/*<p className="product-lowest-kcal">lowest_kcal: {this.state["lowest_kcal"]}</p>*/}
    {/*<p className="product-description">Site-text: {this.state["site_text"]}</p>*/}
        </div>
        }
         
      }
}

export default Product