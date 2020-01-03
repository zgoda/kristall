import { Component } from 'preact';

class UserSelector extends Component {
  state = { users: [], value: '' };

  componentDidMount() {
    const url = '/api/user';
    fetch(url)
      .then((res) => res.json())
      .then((data) => this.setState({ users: data || []}));
  };

  shouldComponentUpdate() {
    return Boolean(this.state.users);
  };

  onInput = (e) => {
    this.setState({ value: e.target.value });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    if (this.state.value !== 'none') {
      this.props.onUserSet(this.state.value);
    }
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

class UserForm extends Component {
  state = { user: '', name: '' };

  onInput = (e) => {
    this.setState({ name: e.target.value })
  }

  handleSubmit = (e) => {
    e.preventDefault();
    const url = '/api/user';
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name: this.state.name }),
    })
      .then((res) => res.json())
      .then((data) => {
        this.setState({ user: data, name: '' });
        this.props.onUserSet(data.pk);
      })
  };

  render(_, { name }) {
    return (
      <div>
        <h2>Create new user</h2>
        <form onSubmit={this.handleSubmit}>
          <input type="text" value={name} onInput={this.onInput} />
          <button type="submit">create</button>
        </form>
      </div>
    );
  }
};

class TodoList extends Component {
  state = { todos: [] };
};

class Home extends Component {
  state = { user: '' };

  handleUserSet = (user) => {
    this.setState({ user: user });
    console.log(user);
  };

  render() {
    return (
      <div>
        <h1>Todos</h1>
        <UserSelector onUserSet={this.handleUserSet} />
        <UserForm onUserSet={this.handleUserSet} />
        <TodoList user={user} />
      </div>
    );
  };
};

export default Home;
