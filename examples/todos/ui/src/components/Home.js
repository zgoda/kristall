import { Component } from 'preact';

class UserSelector extends Component {
  state = { users: [], value: '' };

  async componentDidMount() {
    const users = await this.fetchUsers();
    if (users.length !== this.state.users.length) {
      this.setState({ users: users || [] });
    }
  }

  onInput = (e) => {
    this.setState({ value: e.target.value });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    if (this.state.value !== 'none') {
      this.props.onUserSet(this.state.value, false);
    }
  };

  async fetchUsers() {
    const url = '/api/user';
    const res = await fetch(url);
    const data = await res.json();
    return data;    
  }

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
        this.props.onUserSet(data.pk, true);
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

  render() {
    return (
      <div>
        <h2>Items to do</h2>
      </div>
    );
  };
};

function TodoForm() {
  return (
    <div>
      <h2>Add new todo item</h2>
    </div>
  );
};

function UserInfo({ user }) {
  if (user) {
    return (
      <div>
        <p>Welcome, {user.name}</p>
      </div>
    );
  } else {
    return <div></div>
  }
};

class Home extends Component {
  state = { user: {}, isNew: false };

  handleUserSet = (user, isNew) => {
    const url = `/api/user/${user}`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        this.setState({ user: data, isNew: isNew });
        console.log(user);    
      })
  };

  render() {
    return (
      <div>
        <h1>Todos</h1>
        <UserSelector onUserSet={this.handleUserSet} />
        <UserForm onUserSet={this.handleUserSet} />
        <UserInfo user={this.state.user} />
        <div class="flex two">
          <TodoList user={this.state.user} />
          <TodoForm />
        </div>
      </div>
    );
  };
};

export default Home;
