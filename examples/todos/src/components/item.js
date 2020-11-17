const TodoItem = (({ todo }) => {
  if (todo) {
    let added = new Date(todo.dateAdded);
    return (
      <>
        <h2>{todo.title}</h2>
        <p>{todo.description}</p>
        <p>created: {added.toLocaleString()}</p>
      </>
    )
  }
  return <></>
});

export { TodoItem };
