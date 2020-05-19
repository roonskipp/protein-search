import React, { Component } from 'react'
import Switch from "react-switch";

class NutritionSwitch extends Component{
    constructor(props) {
        super(props);
        this.state = { checked: props.checked };
      }

      handleChange = (checked) => {
        console.log("switch")
        this.setState({ checked }, () => this.props.handleSwitchChange(this.state.checked));
      }

      render() {
          return <div className="nutrition-switch">
             <label>
               <div>
               <span>Search for nutritional information</span>
               </div>
               <div>
               <Switch onChange={this.handleChange} checked={this.state.checked} />
               </div>
      </label>
      </div>
      }
}

export default NutritionSwitch