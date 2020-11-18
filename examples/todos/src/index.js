import { useEffect, useState } from 'preact/hooks';
import './style';
import { TodoList } from './components/list';
import { TodoItem } from './components/item';
import { TodoForm } from './components/form';

export default function App() {
  const [todos, setTodos] = useState([]);
  const [selected, setSelected] = useState(0);

  useEffect(() => {
    const url = '/api/todos';
    fetch(url)
      .then((resp) => resp.json())
      .then((data) => {
        setTodos(data.todos);
        if (data.todos.length > 0) {
          setSelected(0);
        }
      })
  }, []);

  const newTodoHandler = (({ todo }) => {
    let newTodos = todos.slice();
    newTodos.push(todo);
    setTodos(newTodos);
  });

  return (
    <div class="content">
      <h1>My Things To Do</h1>
      <div class="container">
        <div class="column">
          <div class="cell rowspan">
            <TodoList todos={todos} setSelected={setSelected} />
          </div>
        </div>
        <div class="column">
          <div class="cell">
            <TodoItem todo={todos[selected]} />
          </div>
          <div class="cell">
            <TodoForm setNewTodo={newTodoHandler} />
          </div>
        </div>
      </div>
    </div>
  )
}
