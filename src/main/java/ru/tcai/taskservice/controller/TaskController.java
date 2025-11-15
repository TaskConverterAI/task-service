package ru.tcai.taskservice.controller;

import ru.tcai.taskservice.dto.request.TaskRequest;
import ru.tcai.taskservice.dto.response.TaskResponse;
import ru.tcai.taskservice.dto.request.UpdateTaskRequest;
import ru.tcai.taskservice.service.TaskService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/task")
@RequiredArgsConstructor
public class TaskController {

    public TaskService taskService;

    @PostMapping("/create")
    public ResponseEntity<TaskResponse> createTask(@RequestBody TaskRequest taskRequest) {
        TaskResponse response = taskService.createTask(taskRequest);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/get/{id}")
    public ResponseEntity<TaskResponse> getTaskById(@PathVariable Long id) {
        TaskResponse response = taskService.getTaskById(id);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/author/{authorId}")
    public ResponseEntity<List<TaskResponse>> getTasksByAuthorId(@PathVariable Long authorId) {
        List<TaskResponse> response = taskService.getTasksByAuthorId(authorId);
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

    @PutMapping("/update/{id}")
    public ResponseEntity<TaskResponse> updateTask(@PathVariable Long id,
                                                   @RequestBody UpdateTaskRequest updateTaskRequest) {
        TaskResponse response = taskService.updateTask(id, updateTaskRequest);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/delete/{id}")
    public ResponseEntity<Void> deleteTask(@PathVariable Long id) {
        taskService.deleteTask(id);
        return ResponseEntity.noContent().build();
    }
}
