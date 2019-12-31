import { h, Component } from 'preact';
import { Router } from 'preact-router';

import Home from '../routes/home';
import Poll from '../routes/poll';

export default class App extends Component {
  
  handleRoute = (e) => {
    this.currentUrl = e.url;
  };

  render() {
    return (
      <div id="app">
        <Router onChange={this.handleRoute}>
          <Home path="/" />
          <Poll path="/poll/:poll_id" />
        </Router>
      </div>
    );
  }
}
