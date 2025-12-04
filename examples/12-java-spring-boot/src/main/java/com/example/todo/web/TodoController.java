package com.example.todo.web;

import com.example.todo.model.Todo;
import com.example.todo.repo.TodoRepository;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/api/todos")
@CrossOrigin(origins = "*")
public class TodoController {
    private final TodoRepository repo;

    public TodoController(TodoRepository repo) {
        this.repo = repo;
    }

    @GetMapping
    public List<Todo> all() {
        return repo.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Todo> one(@PathVariable Long id) {
        return repo.findById(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Todo> create(@Valid @RequestBody Todo incoming) {
        incoming.setId(null);
        Todo saved = repo.save(incoming);
        return ResponseEntity.created(URI.create("/api/todos/" + saved.getId())).body(saved);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Todo> update(@PathVariable Long id, @Valid @RequestBody Todo incoming) {
        return repo.findById(id)
                .map(existing -> {
                    existing.setTitle(incoming.getTitle());
                    existing.setCompleted(incoming.isCompleted());
                    return ResponseEntity.ok(repo.save(existing));
                })
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PatchMapping("/{id}")
    public ResponseEntity<Todo> patch(@PathVariable Long id, @RequestBody Todo incoming) {
        return repo.findById(id)
                .map(existing -> {
                    if (incoming.getTitle() != null) existing.setTitle(incoming.getTitle());
                    existing.setCompleted(incoming.isCompleted());
                    return ResponseEntity.ok(repo.save(existing));
                })
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        if (!repo.existsById(id)) return ResponseEntity.notFound().build();
        repo.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
