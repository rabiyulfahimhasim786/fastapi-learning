import { useState,useEffect} from 'react';

function App() {
    const [todos,setTodos] = useState([]);
    const [newTodo,setNewTodo] =useState('');
    const API_URL = 'http://localhost:8000/todos';

    //1. fetch all todos  on load
    const fetchTodos = async () =>{
        try {
            const response = await fetch(API_URL);
            const data = await response.json();
            setTodos(data);

        }   catch (error) {
            console.error("Error fetching data:", error);
        }

    }
};

useEffect(() =>{
    fetchTodos();
},[]);


// 2. Create a new todo
const addTodo= async (e) => {
    e.preventDefault();
    if (!newTodo.trim()) return;
    try {
        const response = await fetch(API_URL,{
            method: 'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify({title:newTodo,completed:false}),
        });
    if (response.ok) {
        setNewTodo('');
        fetchTodos();//Refresh list
    }
    } catch (error) {
        console.error("Error adding todo:",error);
    }
};

//3. Toggle Complete Staus
const toggleComplete  = async (todo) =>{
    try{
        await fetch('${API_URL}/${todo.id}',{
            method:'PUT',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({title:todo.title,completed:!todo.completed}),
        });

        fetchTodos();
    }   catch (error) {
        console.error("Error toggling todo:",error);
    }
}

//4. Delete a todo
const deleteTodo = async (id) =>{
    try{
        await fetch('${API_URL}/${id}',{method:'DELETE'});
        fetchTodos();
    } catch (error) {
        console.error("Error deleting todo:",error);
    }
};


 return (
    <div style={{ maxWidth: '500px', margin: '50px auto', fontFamily: 'Arial, sans-serif', padding: '0 20px' }}>
      <h2>📝 FastAPI + React Todo</h2>
      
      {/* Input Form */}
      <form onSubmit={addTodo} style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="What needs to be done?"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          style={{ flex: 1, padding: '8px', fontSize: '16px' }}
        />
        <button type="submit" style={{ padding: '8px 16px', cursor: 'pointer' }}>Add</button>
      </form>

      {/* Todo List */}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {todos.map((todo) => (
          <li key={todo.id} style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '10px',
            borderBottom: '1px solid #eee',
            background: todo.completed ? '#f9f9f9' : 'transparent'
          }}>
            <span 
              onClick={() => toggleComplete(todo)}
              style={{ 
                textDecoration: todo.completed ? 'line-through' : 'none', 
                color: todo.completed ? '#888' : '#000',
                cursor: 'pointer',
                flex: 1
              }}
            >
              {todo.title}
            </span>
            <button 
              onClick={() => deleteTodo(todo.id)} 
              style={{ backgroundColor: '#ff4d4d', color: 'white', border: 'none', padding: '5px 10px', cursor: 'pointer', borderRadius: '3px' }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
