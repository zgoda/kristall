import { Component } from 'preact';

class UserSelector extends Component {
  state = { users: [], value: '' };

  componentDidMount() {
    const url = '/api/user';
    fetch(url)
      .then(res => res.json())
      .then(data => this.setState({ users: data || []}))
  };

  shouldComponentUpdate() {
    return Boolean(this.state.users);
  }

  onInput = (e) => {
    this.setState({ value: e.target.value })
  }

  render(_, { value }) {
    return (
      <div>
        <h2>Select user or create new</h2>
        <select value={value} onInput={this.onInput}>
          {this.state.users.map(user => (
          <option key={user.pk} value={user.pk}>{user.name}</option>
          ))}
        </select>
      </div>
    );
  }
}

const Home = () => (
	<div>
		<h1>Todos</h1>
    <UserSelector />
	</div>
);

export default Home;
