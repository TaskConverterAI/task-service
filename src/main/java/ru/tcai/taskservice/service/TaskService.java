package ru.tcai.taskservice.service;

import ru.tcai.taskservice.dto.request.*;
import ru.tcai.taskservice.dto.response.*;

import java.util.List;

public interface TaskService {
    TaskResponse createTask(TaskRequest taskRequest);

    TaskResponse getTaskById(Long id);

    List<TaskResponse> getPersonalTasksByAuthorId(Long authorId);

    List<TaskResponse> getTasksByAuthorId(Long authorId);

    List<TaskResponse> getTasksByGroupId(Long groupId);

    List<TaskResponse> getTasksByDoerId(Long doerId);

    TaskDetailsResponse getTaskDetailsById(Long taskId);

    TaskResponse updateTask(Long id, UpdateTaskRequest updateTaskRequest);

    CommentResponse addCommentToTask(Long taskId, CommentRequest commentRequest);

    void deleteComment(Long id);

    void deleteTask(Long id);

    NoteResponse createNote(NoteRequest noteRequest);

    void deleteNote(Long id);

    NoteResponse updateNote(Long id, UpdateNoteRequest updateNoteRequest);

    NoteResponse getNoteById(Long id);

    List<NoteResponse> getPersonalNotesByAuthorId(Long authorId);

    List<NoteResponse> getNotesByAuthorId(Long authorId);

    List<NoteResponse> getNotesByGroupId(Long groupId);

    NoteDetailsResponse getNoteDetailsById(Long id);
}