import { Component } from 'preact';

import Home from './components/Home';

export default class App extends Component {
  
  render() {
    return (
      <div id="app">
        <Home />
      </div>
    );
  }
}
