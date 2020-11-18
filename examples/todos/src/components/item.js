import { CheckSquare } from 'preact-feather';

const TodoItem = (({ todo, completeHandler }) => {

  const checkboxClickHandler = ((e) => {
    e.preventDefault();
    return false;
  });

  const completeButtonClickHandler = ((e) => {
    const url = `/api/todo/${todo.id}`;
    fetch(url, {
      method: 'PUT',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ isComplete: true })
    })
      .then((resp) => resp.json())
      .then((data) => {
        console.log(data);
        completeHandler({ todo: data });
      })
      .catch((err) => console.error(err))
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
        {!todo.isComplete && <p><button type="button" class="button secondary" onClick={completeButtonClickHandler}><CheckSquare size={16} /> Complete task</button></p>}
      </>
    )
  }
  return <></>
});

export { TodoItem };
