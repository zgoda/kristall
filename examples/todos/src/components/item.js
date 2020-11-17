import { CheckSquare } from 'preact-feather';

const TodoItem = (({ todo }) => {

  const checkboxClickHandler = ((e) => {
    e.preventDefault();
    return false;
  });

  if (todo) {
    const added = new Date(todo.dateAdded).toLocaleString();
    let completed;
    if (todo.dateCompleted) {
      completed = new Date(todo.dateCompleted).toLocaleString()
    } else {
      completed = 'not yet completed'
    }
    return (
      <>
        <h2>{todo.title}</h2>
        <p>{todo.description}</p>
        <p>created: {added}</p>
        <p>is completed: <input type="checkbox" checked={todo.isComplete} onClick={checkboxClickHandler} /></p>
        <p>completion date: {completed}</p>
        {!todo.isComplete && <p><button type="button"><CheckSquare size={12} /> Complete task</button></p>}
      </>
    )
  }
  return <></>
});

export { TodoItem };
