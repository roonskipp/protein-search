import React, { Component } from 'react'

class SearchBar extends Component {
  constructor (props) {
    super(props)
    this.state = {
      search: '',
      SearchCallback : props.SearchCallback
    }
  }

  handleSearch (e) {
    this.setState({ search: e.target.value }, () => this.props.SearchCallback(this.state.search))
    
  }

  handleGoClick () {
    this.props.SearchCallback(this.state.search);
  }

  render () {
    return (
      <div className='searchbar-container'>
        <form onSubmit={e => e.preventDefault()}>
          <input
            type='text'
            size='45'
            placeholder='Search for proteinbar'
            onChange={this.handleSearch.bind(this)}
            value={this.state.search} />
          <button
            type='submit'
            onClick={this.handleGoClick.bind(this)}>
            Search
          </button>
        </form>
      </div>
    )
  }
}

export default SearchBar