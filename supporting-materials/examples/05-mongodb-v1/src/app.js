import express from 'express';
import mongoose from 'mongoose';
import morgan from 'morgan';

const app = express();
const PORT = process.env.PORT || 3000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://mongo:27017/todos';

// Middleware
app.use(morgan('dev'));
app.use(express.urlencoded({ extended: true })); // for form posts
app.use(express.static('public'));

// Mongoose model
const todoSchema = new mongoose.Schema({
  text: { type: String, required: true, trim: true },
  done: { type: Boolean, default: false },
  createdAt: { type: Date, default: Date.now }
});

const Todo = mongoose.model('Todo', todoSchema);

// Views (plain HTML)
function layout(title, body) {
  return `<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${title}</title>
  <style>
    body { font-family: system-ui, Arial, sans-serif; margin: 2rem auto; max-width: 720px; padding: 0 1rem; }
    header { display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; }
    h1 { font-size: 1.6rem; }
    form { display: inline; }
    ul { list-style: none; padding: 0; }
    li { display:flex; align-items:center; justify-content:space-between; gap: .5rem; padding: .5rem .75rem; border: 1px solid #ddd; border-radius: 6px; margin:.5rem 0; }
    .done { text-decoration: line-through; color: #777; }
    .actions form { display:inline; }
    input[type=text] { padding:.5rem; width: 70%; }
    button { padding:.4rem .7rem; border:1px solid #ccc; background:#f7f7f7; border-radius:6px; cursor:pointer; }
    button.primary { background: #1e88e5; color: white; border-color:#1b74c4; }
    small { color:#666; }
    footer { margin-top:2rem; color:#666; font-size:.9rem; }
    .count { color:#444; }
  </style>
</head>
<body>
  ${body}
  <footer>
    <small>MongoDB demo: simple To-Do app. Usługi: web, mongo, mongo-express.</small>
  </footer>
</body>
</html>`;
}

function indexView(items) {
  const remaining = items.filter(i => !i.done).length;
  const total = items.length;
  const list = items.map(i => `
    <li>
      <span class="${i.done ? 'done' : ''}">${escapeHtml(i.text)}</span>
      <span class="actions">
        <form method="post" action="/toggle/${i._id}"><button>${i.done ? '↩︎ Przywróć' : '✓ Zakończ'}</button></form>
        <form method="post" action="/delete/${i._id}" onsubmit="return confirm('Usunąć zadanie?');"><button>🗑️ Usuń</button></form>
      </span>
    </li>`).join('');
  return layout('To-Do + MongoDB', `
    <header>
      <h1>Lista zadań (MongoDB)</h1>
      <small class="count">${remaining}/${total} do zrobienia</small>
    </header>
    <section>
      <form method="post" action="/add">
        <input type="text" name="text" placeholder="Nowe zadanie..." required />
        <button class="primary" type="submit">Dodaj</button>
      </form>
    </section>
    <section>
      <ul>
        ${list || '<li><small>Brak zadań — dodaj pierwsze powyżej ✨</small></li>'}
      </ul>
    </section>
  `);
}

function escapeHtml(str) {
  return String(str)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

// Routes
app.get('/healthz', (_req, res) => {
  res.json({ ok: true, mongo: mongoose.connection.readyState });
});

app.get('/', async (_req, res, next) => {
  try {
    const items = await Todo.find().sort({ createdAt: -1 }).lean();
    res.type('html').send(indexView(items));
  } catch (err) { next(err); }
});

app.post('/add', async (req, res, next) => {
  try {
    const text = (req.body.text || '').trim();
    if (text) {
      await Todo.create({ text });
    }
    res.redirect('/');
  } catch (err) { next(err); }
});

app.post('/toggle/:id', async (req, res, next) => {
  try {
    const id = req.params.id;
    const todo = await Todo.findById(id);
    if (todo) {
      todo.done = !todo.done;
      await todo.save();
    }
    res.redirect('/');
  } catch (err) { next(err); }
});

app.post('/delete/:id', async (req, res, next) => {
  try {
    await Todo.findByIdAndDelete(req.params.id);
    res.redirect('/');
  } catch (err) { next(err); }
});

// Error handler
// eslint-disable-next-line no-unused-vars
app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(500).send('<pre>Wewnętrzny błąd serwera</pre>');
});

// Start server after DB connected
async function start() {
  try {
    await mongoose.connect(MONGODB_URI, { dbName: 'todos' });
    console.log('Połączono z MongoDB');

    // Seed if empty
    const count = await Todo.estimatedDocumentCount();
    if (count === 0) {
      await Todo.insertMany([
        { text: 'Zapoznaj się z aplikacją', done: false },
        { text: 'Dodaj własne zadanie', done: false }
      ]);
      console.log('Dodano przykładowe zadania.');
    }

    app.listen(PORT, () => console.log(`Serwer działa na porcie ${PORT}`));
  } catch (e) {
    console.error('Błąd połączenia z MongoDB:', e);
    process.exit(1);
  }
}

start();
