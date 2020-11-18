import { useState } from 'preact/hooks';
import { Plus } from 'preact-feather';

const TodoForm = (({ setNewTodo }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const submitHandler = ((e) => {
    e.preventDefault();
    const url = '/api/todos';
    fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title, description })
    })
      .then((resp) => resp.json())
      .then((data) => {
        console.log(data);
        setTitle('');
        setDescription('');
        setNewTodo({ todo: data });
      })
      .catch((err) => console.error(err));
  })

  return (
    <>
      <h2>New thing to do</h2>
      <form onSubmit={submitHandler}>
        <div>
          <label for="title">Title</label>
          <input type="text" name="title" value={title} onInput={(e) => setTitle(e.target.value)} />
        </div>
        <div>
          <label for="description">Description</label>
          <textarea name="description" onInput={(e) => setDescription(e.target.value)} value={description} />
        </div>
        <div>
          <button type="submit"><Plus size={12} /> Add todo</button>
        </div>
      </form>
    </>
  )
});

export { TodoForm };
