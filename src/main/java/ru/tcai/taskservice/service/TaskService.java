package ru.tcai.taskservice.service;


import ru.tcai.taskservice.dto.request.TaskRequest;
import ru.tcai.taskservice.dto.response.TaskResponse;
import ru.tcai.taskservice.dto.request.UpdateTaskRequest;

import java.util.List;

public interface TaskService {
    TaskResponse createTask(TaskRequest taskRequest);

    TaskResponse getTaskById(Long id);

    List<TaskResponse> getTasksByAuthorId(Long authorId);

    List<TaskResponse> getTasksByGroupId(Long groupId);

    List<TaskResponse> getTasksByDoerId(Long doerId);

    TaskResponse updateTask(Long id, UpdateTaskRequest updateTaskRequest);

    void deleteTask(Long id);
}