package ru.tcai.taskservice.controller;

import ru.tcai.taskservice.dto.request.*;
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
@RequestMapping("/api/tasks")
@RequiredArgsConstructor
public class TaskController {

    private final TaskService taskService;

    @PostMapping("/create")
    public ResponseEntity<TaskResponse> createTask(@RequestBody TaskRequest taskRequest) {
        TaskResponse response = taskService.createTask(taskRequest);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/get/{taskId}")
    public ResponseEntity<TaskResponse> getTaskById(@PathVariable Long taskId) {
        TaskResponse response = taskService.getTaskById(taskId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/get/user/{userId}")
    public ResponseEntity<List<TaskResponse>> getTasksByAuthorId(@PathVariable Long userId) {
        List<TaskResponse> response = taskService.getTasksByAuthorId(userId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/get/group/{groupId}")
    public ResponseEntity<List<TaskResponse>> getTasksByGroupId(@PathVariable Long groupId) {
        List<TaskResponse> response = taskService.getTasksByGroupId(groupId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/get/doer/{doerId}")
    public ResponseEntity<List<TaskResponse>> getTasksByDoerId(@PathVariable Long doerId) {
        List<TaskResponse> response = taskService.getTasksByDoerId(doerId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/get/details/{taskId}")
    public ResponseEntity<TaskDetailsResponse> getTaskDetailsById(@PathVariable Long taskId) {
        TaskDetailsResponse response = taskService.getTaskDetailsId(taskId);
        return ResponseEntity.ok(response);
    }

    @PutMapping("/update/{taskId}")
    public ResponseEntity<TaskResponse> updateTask(@PathVariable Long taskId,
                                                   @RequestBody UpdateTaskRequest updateTaskRequest) {
        TaskResponse response = taskService.updateTask(taskId, updateTaskRequest);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/delete/{id}")
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

    @PutMapping("/update/subtask/{subtaskId}/status")
    public ResponseEntity<SubtaskResponse> updateSubtaskStatus(@PathVariable Long subtaskId,
                                                            @RequestBody UpdateSubtaskStatusRequest updateSubtaskStatusRequest) {
        SubtaskResponse response = taskService.updateSubtaskStatus(subtaskId, updateSubtaskStatusRequest);
        return ResponseEntity.ok(response);
    }
}
