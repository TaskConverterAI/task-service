package ru.tcai.taskservice.service;

import ru.tcai.taskservice.dto.request.*;
import ru.tcai.taskservice.dto.response.*;
import ru.tcai.taskservice.entity.*;
import ru.tcai.taskservice.exception.CommentNotFoundException;
import ru.tcai.taskservice.exception.SubtaskNotFoundException;
import ru.tcai.taskservice.exception.TaskNotFoundException;
import ru.tcai.taskservice.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class TaskServiceImpl implements TaskService {

    private final TaskRepository taskRepository;
    private final LocationRepository locationRepository;
    private final LocationPointRepository locationPointRepository;
    private final ReminderRepository reminderRepository;
    private final LinkedTaskRepository linkedTaskRepository;
    private final CommentRepository commentRepository;

    @Override
    public TaskResponse createTask(TaskRequest taskRequest) {
        log.info("Creating task: {}", taskRequest.getTitle());

        Long locationPointId = null;
        if (taskRequest.getLocation() != null) {
            LocationPoint locationPoint = LocationPoint.builder()
                    .latitude(taskRequest.getLocation().getLatitude())
                    .longitude(taskRequest.getLocation().getLongitude())
                    .name(taskRequest.getLocation().getLocationName())
                    .build();
            LocationPoint savedLocationPoint = locationPointRepository.save(locationPoint);
            locationPointId = savedLocationPoint.getId();
        }

        Long locationId = null;
        if (locationPointId != null) {
            Location location = Location.builder()
                    .point_id(locationPointId)
                    .remindByLocation(taskRequest.getLocation().getRemindByLocation())
                    .build();
            Location savedLocation = locationRepository.save(location);
            locationId = savedLocation.getId();
        }

        Long reminderId = null;
        if (taskRequest.getDeadline() != null) {
            Reminder reminder = Reminder.builder()
                    .time(taskRequest.getDeadline().getTime())
                    .remindByTime(taskRequest.getDeadline().getRemindByTime())
                    .build();
            Reminder savedReminder = reminderRepository.save(reminder);
            reminderId = savedReminder.getId();
        }

        LocalDateTime now = LocalDateTime.now();

        Task task = Task.builder()
                .title(taskRequest.getTitle())
                .description(taskRequest.getDescription())
                .taskType(taskRequest.getTaskType())
                .location_id(locationId)
                .deadline_id(reminderId)
                .authorId(taskRequest.getAuthorId())
                .groupId(taskRequest.getGroupId())
                .doerId(taskRequest.getDoerId())
                .status("UNDONE")
                .createdAt(now)
                .updatedAt(now)
                .build();


        log.info("Try to write task");
        Task savedTask = taskRepository.save(task);
        log.info("Created task with ID: {}", savedTask.getId());

        return mapTaskToTaskResponse(savedTask);
    }

    @Override
    public TaskResponse getTaskById(Long id) {
        log.info("Getting task by ID: {}", id);

        Task task = taskRepository.findById(id).orElse(null);

        return mapTaskToTaskResponse(task);
    }

    @Override
    public List<TaskResponse> getPersonalTasksByAuthorId(Long authorId) {
        log.info("Getting personal tasks by author ID: {}", authorId);

        List<Task> tasks = taskRepository.findByGroupIdIsNullAndAuthorId(authorId);
        return tasks.stream()
                .map(this::mapTaskToTaskResponse)
                .collect(Collectors.toList());
    }

    @Override
    public List<TaskResponse> getTasksByAuthorId(Long authorId) {
        log.info("Getting tasks by author ID: {}", authorId);

        List<Task> tasks = taskRepository.findByAuthorId(authorId);
        return tasks.stream()
                .map(this::mapTaskToTaskResponse)
                .collect(Collectors.toList());
    }

    @Override
    public List<TaskResponse> getTasksByGroupId(Long groupId) {
        log.info("Getting tasks by group ID: {}", groupId);

        List<Task> tasks = taskRepository.findByGroupId(groupId);
        return tasks.stream()
                .map(this::mapTaskToTaskResponse)
                .collect(Collectors.toList());
    }

    @Override
    public List<TaskResponse> getTasksByDoerId(Long doerId) {
        log.info("Getting tasks by doer ID: {}", doerId);

        List<Task> tasks = taskRepository.findByDoerId(doerId);
        return tasks.stream()
                .map(this::mapTaskToTaskResponse)
                .collect(Collectors.toList());
    }

    @Override
    public TaskDetailsResponse getTaskDetailsById(Long taskId) {
        log.info("Getting task by ID: {}", taskId);

        Task task = taskRepository.findById(taskId)
                .orElseThrow(() -> new TaskNotFoundException("Task not found with id: " + taskId));

        log.info("Task found: {}", task);
        return mapTaskToTaskDetailsResponse(task);
    }

    @Override
    public SubtaskResponse createSubtask(Long taskId, CreateSubtaskRequest createSubtaskRequest) {
        log.info("Creating subtask for task ID: {}", taskId);
        Task task = taskRepository.findById(taskId)
                .orElseThrow(() -> new TaskNotFoundException("Task not found with id: " + taskId));
        Task subtask = Task.builder()
                .description(createSubtaskRequest.getText())
                .taskType(Long.valueOf(1))
                .authorId(task.getAuthorId())
                .groupId(task.getGroupId())
                .doerId(task.getDoerId())
                .status("UNDONE")
                .build();
        taskRepository.save(subtask);
        log.info("Created subtask with ID: {}", subtask.getId());
        return mapSubtaskToSubtaskResponse(subtask);
    }

    @Override
    public SubtaskResponse updateSubtaskStatus(Long subtaskId, UpdateSubtaskStatusRequest updateSubtaskStatusRequest) {
        log.info("Updating subtask status with ID: {}", subtaskId);
        Task subtask = taskRepository.findById(subtaskId)
                .orElseThrow(() -> new SubtaskNotFoundException("Subtask not found with id: " + subtaskId));
        subtask.setStatus(updateSubtaskStatusRequest.getStatus());
        subtask.setUpdatedAt(LocalDateTime.now());
        taskRepository.save(subtask);
        log.info("Updated subtask status with ID: {}", subtaskId);
        return mapSubtaskToSubtaskResponse(subtask);
    }

    @Override
    public TaskResponse updateTask(Long id, UpdateTaskRequest updateTaskRequest) {
        log.info("Updating task with ID: {}", id);

        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new TaskNotFoundException("Task not found with id: " + id));

        // Update location if provided
        if (updateTaskRequest.getLocation() != null) {
            // First delete existing location and point if they exist
            if (task.getLocation_id() != null) {
                Location existingLocation = locationRepository.findById(task.getLocation_id()).orElse(null);
                if (existingLocation != null && existingLocation.getPoint_id() != null) {
                    locationPointRepository.deleteById(existingLocation.getPoint_id());
                }
                locationRepository.deleteById(task.getLocation_id());
            }

            // Create new location point
            LocationPoint locationPoint = LocationPoint.builder()
                    .latitude(updateTaskRequest.getLocation().getLatitude())
                    .longitude(updateTaskRequest.getLocation().getLongitude())
                    .name(updateTaskRequest.getLocation().getLocationName())
                    .build();
            LocationPoint savedLocationPoint = locationPointRepository.save(locationPoint);

            // Create new location
            Location location = Location.builder()
                    .point_id(savedLocationPoint.getId())
                    .remindByLocation(updateTaskRequest.getLocation().getRemindByLocation())
                    .build();
            Location savedLocation = locationRepository.save(location);

            task.setLocation_id(savedLocation.getId());
        }

        // Update reminder if provided
        if (updateTaskRequest.getDeadline() != null) {
            if (task.getDeadline_id() != null) {
                reminderRepository.deleteById(task.getDeadline_id());
            }

            Reminder reminder = Reminder.builder()
                    .time(updateTaskRequest.getDeadline().getTime())
                    .remindByTime(updateTaskRequest.getDeadline().getRemindByTime())
                    .build();
            Reminder savedReminder = reminderRepository.save(reminder);
            task.setDeadline_id(savedReminder.getId());
        }

        // Update other fields
        if (updateTaskRequest.getTitle() != null) {
            task.setTitle(updateTaskRequest.getTitle());
        }
        if (updateTaskRequest.getDescription() != null) {
            task.setDescription(updateTaskRequest.getDescription());
        }
        if (updateTaskRequest.getTaskType() != null) {
            task.setTaskType(updateTaskRequest.getTaskType());
        }
        if (updateTaskRequest.getGroupId() != null) {
            task.setGroupId(updateTaskRequest.getGroupId());
        }
        if (updateTaskRequest.getDoerId() != null) {
            task.setDoerId(updateTaskRequest.getDoerId());
        }

        task.setUpdatedAt(LocalDateTime.now());

        Task updatedTask = taskRepository.save(task);
        log.info("Updated task with ID: {}", updatedTask.getId());

        return mapTaskToTaskResponse(updatedTask);
    }

    @Override
    public CommentResponse addCommentToTask(Long taskId, CommentRequest commentRequest) {
        log.info("Writing comment to task with ID: {}", taskId);

        Task task = taskRepository.findById(taskId)
                .orElseThrow(() -> new TaskNotFoundException("Task not found with id: " + taskId));

        Comment comment = Comment.builder()
                .taskId(taskId)
                .authorId(commentRequest.getAuthorId())
                .text(commentRequest.getText())
                .build();

        Comment savedComment = commentRepository.save(comment);

        task.setUpdatedAt(LocalDateTime.now());
        taskRepository.save(task);

        log.info("Wrote comment to task with ID: {}", taskId);

        return mapCommentToCommentResponse(savedComment);
    }

    @Override
    public void deleteComment(Long id) {
        log.info("Deleting comment with ID: {}", id);

        Comment comment = commentRepository.findById(id)
                .orElseThrow(() -> new CommentNotFoundException("Comment not found with id: " + id));
        commentRepository.delete(comment);

        log.info("Deleted comment with ID: {}", id);
    }

    @Override
    public void deleteTask(Long id) {
        log.info("Deleting task with ID: {}", id);

        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new TaskNotFoundException("Task not found with id: " + id));

        taskRepository.deleteById(id);

        List<LinkedTask> linkedTasks = linkedTaskRepository.findByTaskId(id);
        if (linkedTasks != null) {
            for (LinkedTask linkedTask : linkedTasks) {
                Long linkedTaskId = linkedTask.getLinkedTaskId();
                linkedTaskRepository.deleteByTaskId(linkedTaskId);
                deleteTask(linkedTaskId);
            }
        }

        if (task.getLocation_id() != null) {
            Location location = locationRepository.findById(task.getLocation_id()).orElse(null);
            locationRepository.deleteById(task.getLocation_id());
            if (location != null && location.getPoint_id() != null) {
                locationPointRepository.deleteById(location.getPoint_id());
            }

        }

        if (task.getDeadline_id() != null) {
            reminderRepository.deleteById(task.getDeadline_id());
        }

        List<Comment> comments = commentRepository.findByTaskId(id);
        if (comments != null) {
            commentRepository.deleteAll(comments);
        }

        taskRepository.deleteById(id);
        log.info("Deleted task with ID: {}", id);

    }

    public TaskDetailsResponse mapTaskToTaskDetailsResponse(Task task) {
        if (task == null) {
            return null;
        }

        return TaskDetailsResponse.builder()
                .id(task.getId())
                .title(task.getTitle())
                .description(task.getDescription())
                .taskType(task.getTaskType())
                .authorId(task.getAuthorId())
                .groupId(task.getGroupId())
                .doerId(task.getDoerId())
                .location(mapLocationToLocationResponse(locationRepository.findById(task.getLocation_id()).orElse(null)))
                .deadline(mapReminderToDeadlineResponse(reminderRepository.findById(task.getDeadline_id()).orElse(null)))
                .createdAt(task.getCreatedAt())
                .subtasks(getSubtasks(task).stream().map(this::mapSubtaskToSubtaskResponse).collect(Collectors.toList()))
                .comments(getComments(task).stream().map(this::mapCommentToCommentResponse).collect(Collectors.toList()))
                .build();
    }

    public SubtaskResponse mapSubtaskToSubtaskResponse(Task task) {
        if (task == null) {
            return null;
        }

        return SubtaskResponse.builder()
                .id(task.getId())
                .description(task.getDescription())
                .authorId(task.getAuthorId())
                .groupId(task.getGroupId())
                .doerId(task.getDoerId())
                .createdAt(task.getCreatedAt())
                .updatedAt(task.getUpdatedAt())
                .status(task.getStatus())
                .build();
    }

    public List<Task> getSubtasks(Task task) {
        List<Task> subtasks = new ArrayList<>();
        List<LinkedTask> linkedTasks = linkedTaskRepository.findByTaskId(task.getId());
        for (LinkedTask linkedTask : linkedTasks) {
            Task subtask = taskRepository.findById(linkedTask.getLinkedTaskId()).orElse(null);
            if (subtask != null) {
                subtasks.add(subtask);
            }
        }
        return subtasks;
    }

    public CommentResponse mapCommentToCommentResponse(Comment comment) {
        if (comment == null) {
            return null;
        }

        return CommentResponse.builder()
                .id(comment.getId())
                .taskId(comment.getTaskId())
                .authorId(comment.getAuthorId())
                .text(comment.getText())
                .createdAt(comment.getCreatedAt())
                .build();
    }

    public List<Comment> getComments(Task task) {
        return commentRepository.findByTaskId(task.getId());
    }

    public DeadlineResponse mapReminderToDeadlineResponse(Reminder reminder) {
        if (reminder == null) {
            return null;
        }

        return DeadlineResponse.builder()
                .time(reminder.getTime())
                .remindByTime(reminder.getRemindByTime())
                .build();
    }

    public LocationResponse mapLocationToLocationResponse(Location location) {
        if (location == null) {
            return null;
        }

        LocationPoint locationPoint = locationPointRepository.findById(location.getPoint_id()).orElse(null);

        return LocationResponse.builder()
                .latitude(locationPoint.getLatitude())
                .longitude(locationPoint.getLongitude())
                .locationName(locationPoint.getName())
                .remindByLocation(location.getRemindByLocation() != null ? location.getRemindByLocation() : false)
                .build();
    }

    public Location mapLocationRequestToLocation(LocationRequest locationRequest) {
        if (locationRequest == null) {
            return null;
        }
        return Location.builder()
                .point_id(LocationPoint.builder()
                        .latitude(locationRequest.getLatitude())
                        .longitude(locationRequest.getLongitude())
                        .name(locationRequest.getLocationName())
                        .build().getId())
                .remindByLocation(locationRequest.getRemindByLocation() != null ? locationRequest.getRemindByLocation() : false)
                .build();
    }

    public Reminder mapDeadlineRequestToDeadline(DeadlineRequest deadlineRequest) {
        if (deadlineRequest == null) {
            return null;
        }
        return Reminder.builder()
                .time(deadlineRequest.getTime())
                .remindByTime(deadlineRequest.getRemindByTime() != null ? deadlineRequest.getRemindByTime() : false)
                .build();
    }

    public TaskResponse mapTaskToTaskResponse(Task task) {
        if (task == null) {
            return null;
        }

        LocationRequest locationRequest = null;
        if (task.getLocation_id() != null) {
            Location location = locationRepository.findById(task.getLocation_id()).orElse(null);
            if (location != null && location.getPoint_id() != null) {
                LocationPoint point = locationPointRepository.findById(location.getPoint_id()).orElse(null);
                if (point != null) {
                    locationRequest = LocationRequest.builder()
                            .latitude(point.getLatitude())
                            .longitude(point.getLongitude())
                            .locationName(point.getName())
                            .remindByLocation(location.getRemindByLocation())
                            .build();
                }
            }
        }

        DeadlineRequest reminderRequest = null;
        if (task.getDeadline_id() != null) {
            Reminder reminder = reminderRepository.findById(task.getDeadline_id()).orElse(null);
            if (reminder != null) {
                reminderRequest = DeadlineRequest.builder()
                        .time(reminder.getTime())
                        .remindByTime(reminder.getRemindByTime())
                        .build();
            }
        }

        return TaskResponse.builder()
                .id(task.getId())
                .authorId(task.getAuthorId())
                .title(task.getTitle())
                .description(task.getDescription())
                .taskType(task.getTaskType())
                .location(locationRequest)
                .deadline(reminderRequest)
                .groupId(task.getGroupId())
                .doerId(task.getDoerId())
                .createdAt(task.getCreatedAt())
                .build();
    }
}
