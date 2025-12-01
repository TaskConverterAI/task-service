package ru.tcai.taskservice.controller;

import ru.tcai.taskservice.dto.request.*;
import ru.tcai.taskservice.dto.response.*;
import ru.tcai.taskservice.service.TaskService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/tasks")
@RequiredArgsConstructor
public class TaskController {

    private final TaskService taskService;

    @PostMapping
    public ResponseEntity<TaskResponse> createTask(@RequestBody TaskRequest taskRequest) {
        TaskResponse response = taskService.createTask(taskRequest);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/{taskId}")
    public ResponseEntity<TaskResponse> getTaskById(@PathVariable Long taskId) {
        TaskResponse response = taskService.getTaskById(taskId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/personal/{userId}")
    public ResponseEntity<List<TaskResponse>> getPersonalTasksByAuthorId(@PathVariable Long userId) {
        List<TaskResponse> response = taskService.getPersonalTasksByAuthorId(userId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<TaskResponse>> getTasksByAuthorId(@PathVariable Long userId) {
        List<TaskResponse> response = taskService.getTasksByAuthorId(userId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/group/{groupId}")
    public ResponseEntity<List<TaskResponse>> getTasksByGroupId(@PathVariable Long groupId) {
        List<TaskResponse> response = taskService.getTasksByGroupId(groupId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/doer/{doerId}")
    public ResponseEntity<List<TaskResponse>> getTasksByDoerId(@PathVariable Long doerId) {
        List<TaskResponse> response = taskService.getTasksByDoerId(doerId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/details/{taskId}")
    public ResponseEntity<TaskDetailsResponse> getTaskDetailsById(@PathVariable Long taskId) {
        TaskDetailsResponse response = taskService.getTaskDetailsById(taskId);
        return ResponseEntity.ok(response);
    }

    @PutMapping("/{taskId}")
    public ResponseEntity<TaskResponse> updateTask(@PathVariable Long taskId,
                                                   @RequestBody UpdateTaskRequest updateTaskRequest) {
        TaskResponse response = taskService.updateTask(taskId, updateTaskRequest);
        return ResponseEntity.ok(response);
    }

    @PutMapping("/{taskId}/comment")
    public ResponseEntity<CommentResponse> addCommentToTask(@PathVariable Long taskId,
                                                            @RequestBody CommentRequest commentRequest) {
        CommentResponse response = taskService.addCommentToTask(taskId, commentRequest);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/comment/{id}")
    public ResponseEntity<Void> deleteComment(@PathVariable Long id) {
        taskService.deleteComment(id);
        return ResponseEntity.noContent().build();
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTask(@PathVariable Long id) {
        taskService.deleteTask(id);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/note")
    public ResponseEntity<NoteResponse> createNote(@RequestBody NoteRequest noteRequest) {
        NoteResponse response = taskService.createNote(noteRequest);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/note/personal/{userId}")
    public ResponseEntity<List<NoteResponse>> getPersonalNotesByAuthorId(@PathVariable Long userId) {
        List<NoteResponse> response = taskService.getPersonalNotesByAuthorId(userId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/note/user/{userId}")
    public ResponseEntity<List<NoteResponse>> getNotesByAuthorId(@PathVariable Long userId) {
        List<NoteResponse> response = taskService.getNotesByAuthorId(userId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/note/group/{groupId}")
    public ResponseEntity<List<NoteResponse>> getNotesByGroupId(@PathVariable Long groupId) {
        List<NoteResponse> response = taskService.getNotesByGroupId(groupId);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/note/{id}")
    public ResponseEntity<Void> deleteNote(@PathVariable Long id) {
        taskService.deleteNote(id);
        return ResponseEntity.noContent().build();
    }

    @PutMapping("/note/{id}")
    public ResponseEntity<NoteResponse> updateNote(@PathVariable Long id,
                                                   @RequestBody UpdateNoteRequest updateNoteRequest) {
        NoteResponse response = taskService.updateNote(id, updateNoteRequest);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/note/{id}")
    public ResponseEntity<NoteResponse> getNoteById(@PathVariable Long id) {
        NoteResponse response = taskService.getNoteById(id);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/note/details/{id}")
    public ResponseEntity<NoteDetailsResponse> getNoteDetailsById(@PathVariable Long id) {
        NoteDetailsResponse response = taskService.getNoteDetailsById(id);
        return ResponseEntity.ok(response);
    }

    @PutMapping("/note/{noteId}/comment")
    public ResponseEntity<CommentResponse> addCommentToNote(@PathVariable Long noteId,
                                                            @RequestBody CommentRequest commentRequest) {
        CommentResponse response = taskService.addCommentToNote(noteId, commentRequest);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/note/comment/{id}")
    public ResponseEntity<Void> deleteCommentToNote(@PathVariable Long id) {
        taskService.deleteComment(id);
        return ResponseEntity.noContent().build();
    }
}
