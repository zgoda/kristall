import { useState } from 'preact/hooks';

const TodoList = (({todos, setSelected}) => {
  const [value, setValue] = useState(-1);

  const selectionChanged = ((e) => {
    setValue(e.target.value);
    setSelected(e.target.value);
  });

  return (
    <select size="10" value={value} onChange={selectionChanged}>
      {todos.map((todo, index) => (
        <option key={todo.id} value={index}>{todo.title}</option>
      ))}
    </select>
  )
});

export { TodoList };
