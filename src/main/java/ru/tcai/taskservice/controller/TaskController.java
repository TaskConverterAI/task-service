package ru.tcai.taskservice.controller;

import ru.tcai.taskservice.dto.request.*;
import ru.tcai.taskservice.dto.response.CommentResponse;
import ru.tcai.taskservice.dto.response.SubtaskResponse;
import ru.tcai.taskservice.dto.response.TaskDetailsResponse;
import ru.tcai.taskservice.dto.response.TaskResponse;
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

    @PostMapping("/{taskId}/subtask")
    public ResponseEntity<SubtaskResponse> createSubtask(@PathVariable Long taskId,
                                                         @RequestBody CreateSubtaskRequest createSubtaskRequest) {
        SubtaskResponse response = taskService.createSubtask(taskId, createSubtaskRequest);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PutMapping("/subtask/{subtaskId}/status")
    public ResponseEntity<SubtaskResponse> updateSubtaskStatus(@PathVariable Long subtaskId,
                                                            @RequestBody UpdateSubtaskStatusRequest updateSubtaskStatusRequest) {
        SubtaskResponse response = taskService.updateSubtaskStatus(subtaskId, updateSubtaskStatusRequest);
        return ResponseEntity.ok(response);
    }
}
