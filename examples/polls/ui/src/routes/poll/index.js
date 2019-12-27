import { h, Component } from 'preact';
import style from './style';

class Poll extends Component {
  state = { poll: null };

  async componentDidMount() {
    const url = `/api/poll/${this.props.poll_id}`;
    const resp = await fetch(url);
    const result = await resp.json();
    this.setState({ poll: result });
  };

  render() {
    let title;
    const options = [];
    if (this.state.poll) {
      title = <h1>{this.state.poll.title}</h1>
      if (this.state.poll.options) {
        for (const [index, option] of this.state.poll.options.entries()) {
          options.push(<li key={index}>{option.name}</li>)
        }
      }
    } else {
      title = <h1>Poll</h1>
    }
    return (
      <div class={style.poll}>
        {title}
        <ul>
          {options}
        </ul>
      </div>
    )
  };

};

export default Poll;
