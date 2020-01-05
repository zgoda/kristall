import { Component } from 'preact';

class UserSelector extends Component {
  state = { value: '' };

  onInput = (e) => {
    this.setState({ value: e.target.value });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    if (this.state.value !== 'none') {
      this.props.onUserSet(this.state.value, false);
    }
  };

  render({ users }, { value }) {
    return (
      <div>
        <h2>Select user</h2>
        <form onSubmit={this.handleSubmit}>
          <select value={value} onInput={this.onInput}>
            <option key="none" value="none">---</option>
            {users.map(user => (
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
  state = { name: '' };

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

const TodoItem = ({ item }) => (
  <div>
    <article class="card">
      <header>
        <h3>{item.title}</h3>
      </header>
      <section>{item.description}</section>
      <footer>
        <button>Show details</button>
        <button class="dangerous">Mark as done</button>
      </footer>
    </article>
  </div>
);

function TodoList({ user }) {
  if (user.todos) {
    return (
      <div>
        <h2>Items to do</h2>
        {user.todos.map((item) => (
          <TodoItem key={item.pk} item={item} />
        ))}
      </div>
    )
  } else {
    return (
      <div>
        <h2>Nothing there yet</h2>
      </div>
    )
  };
};

const TodoDetail = () => (
  <div>
    <h2>Item details</h2>
  </div>
)

class TodoForm extends Component {
  state = { item: {} };

  handleSubmit = (e) => {
    e.preventDefault();
    const url = `/api/user/${this.props.user.pk}/todo`;
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(this.state.item),
    })
      .then((res) => res.json())
      .then((data) => {
        this.props.onTodoCreated(data);
      });
  }

  onInput = (e) => {
    let item = Object.assign({}, this.state.item);
    item[e.target.name] = e.target.value;
    this.setState({ item: item });
  };

  toggleDone = (_) => {
    let item = Object.assign({}, this.state.item);
    item.done = !item.done;
    this.setState({ item: item });
  }

  render() {
    return (
      <div>
        <h2>Add new todo item</h2>
        <form onSubmit={this.handleSubmit}>
          <div class="flex two grow">
            <div>
              <label for="title">Title</label>
            </div>
            <div class="four-fifth">
              <input type="text" name="title" value={this.state.item.title} onInput={this.onInput} />
            </div>
            <div>
              <label for="description">Description</label>
            </div>
            <div class="four-fifth">
              <textarea name="description" value={this.state.item.description} onInput={this.onInput} />
            </div>
            <div></div>
            <div class="four-fifth">
              <label>
                <input type="checkbox" checked={this.state.item.done} onClick={this.toggleDone} />
                <span class="checkable">Done</span>
              </label>
            </div>
          </div>
          <button type="submit">Save</button>
        </form>
      </div>
    );
  };
};

function UserInfo({ user }) {
  if (Object.entries(user).length === 0 && user.constructor === Object) {
    return <div></div>
  } else {
    return (
      <div>
        <p>Welcome, {user.name}</p>
      </div>
    );
  };
};

class Home extends Component {
  state = { user: {}, isNew: false, users: [], todos: [] };

  async componentDidMount() {
    const url = '/api/user';
    const resp = await fetch(url);
    const data = await resp.json();
    this.setState({ users: data });
  }

  handleUserSet = (user, isNew) => {
    const url = `/api/user/${user}`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        let state = { user: data, isNew: isNew };
        if (isNew) {
          let users = [... this.state.users];
          users.push(data);
          users.sort((a, b) => a.name.localeCompare(b.name));
          state.users = users;
        };
        this.setState(state);
      });
  };

  handleTodoCreated = (todo) => {
    console.log(todo);
  };

  render() {
    return (
      <div>
        <h1>Todos</h1>
        <UserSelector onUserSet={this.handleUserSet} users={this.state.users} />
        <UserForm onUserSet={this.handleUserSet} />
        <UserInfo user={this.state.user} />
        <div class="flex two">
          <div class="flex one">
            <TodoList user={this.state.user} />
            <TodoDetail />
          </div>
          <TodoForm user={this.state.user} onTodoCreated={this.handleTodoCreated} />
        </div>
      </div>
    );
  };
};

export default Home;
