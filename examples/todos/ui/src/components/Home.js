import { Component } from 'preact';

class UserSelector extends Component {
  state = { users: [], value: '' };

  componentDidMount() {
    const url = '/api/user';
    fetch(url)
      .then(res => res.json())
      .then(data => this.setState({ users: data || []}));
  };

  shouldComponentUpdate() {
    return Boolean(this.state.users);
  };

  onInput = (e) => {
    this.setState({ value: e.target.value });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    console.log(this.state.value);
  };

  render(_, { value }) {
    return (
      <div>
        <h2>Select user</h2>
        <form onSubmit={this.handleSubmit}>
          <select value={value} onInput={this.onInput}>
            <option key="none" value="none">---</option>
            {this.state.users.map(user => (
            <option key={user.pk} value={user.pk}>{user.name}</option>
            ))}
          </select>
          <button type="submit">select</button>
        </form>
      </div>
    );
  };
};

const Home = () => (
	<div>
		<h1>Todos</h1>
    <UserSelector />
	</div>
);

export default Home;
