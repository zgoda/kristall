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

  const completeTodoHandler = (({ todo }) => {
    let newTodos = todos.slice();
    newTodos.forEach((item) => {
      if (item.id === todo.id) {
        item.isComplete = todo.isComplete;
        item.dateCompleted = todo.dateCompleted;
      }
    });
    setTodos(newTodos);
  });

  return (
    <div class="container">
      <h1>My Things To Do</h1>
      <div class="row">
        <div class="col">
          <TodoList todos={todos} setSelected={setSelected} />
        </div>
        <div class="col">
          <TodoItem todo={todos[selected]} completeHandler={completeTodoHandler} />
          <TodoForm setNewTodo={newTodoHandler} />
        </div>
      </div>
    </div>
  )
}
