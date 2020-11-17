import { useState } from 'preact/hooks';

const TodoItem = (({ todo }) => {
  const [completed, setCompleted] = useState(todo && todo.isComplete);

  const toggle = ((e) => {
    setCompleted(!completed);
  });

  if (todo) {
    const added = new Date(todo.dateAdded);
    return (
      <>
        <h2>{todo.title}</h2>
        <p>{todo.description}</p>
        <p>created: {added.toLocaleString()}</p>
        <p>is completed: <input type="checkbox" checked={completed} onClick={toggle} /></p>
      </>
    )
  }
  return <></>
});

export { TodoItem };
