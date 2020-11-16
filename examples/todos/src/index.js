import './style';
import { TodoList } from './components/list';
import { TodoItem } from './components/item';
import { TodoForm } from './components/form';

export default function App() {
  return (
    <div class="container">
      <h1>My Things To Do</h1>
      <TodoList />
      <TodoItem />
      <TodoForm />
    </div>
  )
};
