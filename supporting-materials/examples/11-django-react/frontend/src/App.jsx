import React, { useEffect, useState } from 'react'
import { listTodos, createTodo, toggleTodo, deleteTodo } from './api'

export default function App() {
  const [todos, setTodos] = useState([])
  const [newTitle, setNewTitle] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const load = async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await listTodos()
      setTodos(data)
    } catch (e) {
      setError('Nie udało się pobrać listy zadań')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const add = async (e) => {
    e.preventDefault()
    if (!newTitle.trim()) return
    try {
      await createTodo({ title: newTitle, completed: false })
      setNewTitle('')
      await load()
    } catch {
      setError('Nie udało się dodać zadania')
    }
  }

  const onToggle = async (id) => {
    try {
      await toggleTodo(id)
      await load()
    } catch {
      setError('Nie udało się zmienić statusu')
    }
  }

  const onDelete = async (id) => {
    try {
      await deleteTodo(id)
      await load()
    } catch {
      setError('Nie udało się usunąć zadania')
    }
  }

  return (
    <div style={{ maxWidth: 640, margin: '40px auto', fontFamily: 'system-ui, Arial' }}>
      <h1>Django + React TODO</h1>
      <p style={{ color: '#666' }}>API: {import.meta.env.VITE_API_BASE || 'http://localhost:8000'}</p>
      <form onSubmit={add} style={{ display: 'flex', gap: 8 }}>
        <input
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="Nowe zadanie..."
          style={{ flex: 1, padding: 8 }}
        />
        <button type="submit">Dodaj</button>
      </form>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      {loading ? (
        <p>Ładowanie...</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0, marginTop: 20 }}>
          {todos.map((t) => (
            <li key={t.id} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '6px 0' }}>
              <input type="checkbox" checked={t.completed} onChange={() => onToggle(t.id)} />
              <span style={{ textDecoration: t.completed ? 'line-through' : 'none' }}>{t.title}</span>
              <small style={{ color: '#999', marginLeft: 'auto' }}>{new Date(t.created_at).toLocaleString()}</small>
              <button onClick={() => onDelete(t.id)} style={{ marginLeft: 8 }}>Usuń</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
