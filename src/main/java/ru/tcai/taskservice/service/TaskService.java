package ru.tcai.taskservice.service;


import ru.tcai.taskservice.dto.request.*;
import ru.tcai.taskservice.dto.response.CommentResponse;
import ru.tcai.taskservice.dto.response.SubtaskResponse;
import ru.tcai.taskservice.dto.response.TaskDetailsResponse;
import ru.tcai.taskservice.dto.response.TaskResponse;

import java.util.List;

public interface TaskService {
    TaskResponse createTask(TaskRequest taskRequest);

    TaskResponse getTaskById(Long id);

    List<TaskResponse> getTasksByAuthorId(Long authorId);

    List<TaskResponse> getTasksByGroupId(Long groupId);

    List<TaskResponse> getTasksByDoerId(Long doerId);

    TaskDetailsResponse getTaskDetailsById(Long taskId);

    SubtaskResponse createSubtask(Long taskId, CreateSubtaskRequest createSubtaskRequest);

    SubtaskResponse updateSubtaskStatus(Long subtaskId, UpdateSubtaskStatusRequest updateSubtaskStatusRequest);

    TaskResponse updateTask(Long id, UpdateTaskRequest updateTaskRequest);

    CommentResponse addCommentToTask(Long taskId, CommentRequest commentRequest);

    void deleteTask(Long id);
}