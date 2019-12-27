import { h, Component } from 'preact';
import style from './style';

class Home extends Component {
  state = { polls: [] };

  async componentDidMount() {
    const url = '/api/polls';
    const resp = await fetch(url);
    const result = await resp.json();
    this.setState({ polls: result });
  };

  render() {
    const items = [];
    for (const [index, poll] of this.state.polls.entries()) {
      items.push(<li key={index}>{poll.title}</li>)
    }
    return (
      <div class={style.home}>
        <h1>Polls</h1>
        <p>Current polls</p>
        <ul>
          {items}
        </ul>
      </div>
    )
  };

};

export default Home;
