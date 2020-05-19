import React, { Component } from 'react'

class RadioButtons extends Component{
    constructor (props) {
        super(props)
        this.state = {
            selectedOption : props.optionSelected
        }
      }

      handleOptionChange = (changeEvent) => {
        this.setState({
          selectedOption: changeEvent.target.value
        }, () => this.props.handleOptionChange(this.state.selectedOption));
      }

      render() {
          return <div className="RadioButtons">
              <form>
    <div className="radio">
      <label>
        <input type="radio" value="price" 
                      checked={this.state.selectedOption === 'price'} 
                      onChange={this.handleOptionChange} />
        Price per bar
      </label>
    </div>
    <div className="radio">
      <label>
        <input type="radio" value="discount" 
                      checked={this.state.selectedOption === 'discount'} 
                      onChange={this.handleOptionChange} />
        Discount
      </label>
    </div>
    <div className="radio">
      <label>
        <input type="radio" value="amount" 
                      checked={this.state.selectedOption === 'amount'} 
                      onChange={this.handleOptionChange} />
        Amount of bars
      </label>
    </div>
    <div className="radio">
      <label>
        <input type="radio" value="relevance" 
                      checked={this.state.selectedOption === 'relevance'} 
                      onChange={this.handleOptionChange} />
        Relevance
      </label>
    </div>
    <div className="radio">
      <label>
        <input type="radio" value="kcal" 
                      checked={this.state.selectedOption === 'kcal'} 
                      onChange={this.handleOptionChange} />
        Kcal
      </label>
    </div>
  </form>
          </div>
      }
}

export default RadioButtons