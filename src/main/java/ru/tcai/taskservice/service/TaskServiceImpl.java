package ru.tcai.taskservice.service;

import ru.tcai.taskservice.entity.Location;
import ru.tcai.taskservice.entity.LocationPoint;
import ru.tcai.taskservice.entity.Reminder;
import ru.tcai.taskservice.entity.Task;
import ru.tcai.taskservice.dto.request.DeadlineRequest;
import ru.tcai.taskservice.dto.request.LocationRequest;
import ru.tcai.taskservice.dto.request.TaskRequest;
import ru.tcai.taskservice.dto.request.UpdateTaskRequest;
import ru.tcai.taskservice.dto.response.TaskResponse;
import ru.tcai.taskservice.exception.TaskNotFoundException;
import ru.tcai.taskservice.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class TaskServiceImpl implements TaskService {

    public TaskRepository taskRepository;
    public LocationRepository locationRepository;
    public LocationPointRepository locationPointRepository;
    public ReminderRepository reminderRepository;

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

        Task task = Task.builder()
                .title(taskRequest.getTitle())
                .description(taskRequest.getDescription())
                .taskType(taskRequest.getTaskType())
                .location_id(locationId)
                .deadline_id(reminderId)
                .authorId(taskRequest.getAuthorId())
                .groupId(taskRequest.getGroupId())
                .doerId(taskRequest.getDoerId())
                .build();

        Task savedTask = taskRepository.save(task);
        log.info("Created task with ID: {}", savedTask.getId());

        return mapTaskToTaskResponse(savedTask);
    }

    @Override
    public TaskResponse getTaskById(Long id) {
        log.info("Getting task by ID: {}", id);

        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new TaskNotFoundException("Task not found with id: " + id));

        return mapTaskToTaskResponse(task);
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

        Task updatedTask = taskRepository.save(task);
        log.info("Updated task with ID: {}", updatedTask.getId());

        return mapTaskToTaskResponse(updatedTask);
    }

    @Override
    public void deleteTask(Long id) {
        log.info("Deleting task with ID: {}", id);

        if (!taskRepository.existsById(id)) {
            throw new TaskNotFoundException("Task not found with id: " + id);
        }

        Task task = taskRepository.findById(id).orElseThrow();

        List<Task> allTasks = taskRepository.findAll();
        for (Task t : allTasks) {
            if (t.getLinkedTask().contains(id)) {
                t.getLinkedTask().remove(id);
                taskRepository.save(t);
                break;
            }
        }

        for (Long i : task.getLinkedTask())
        {
            taskRepository.deleteById(i);
        }

        if (task.getLocation_id() != null) {
            Location location = locationRepository.findById(task.getLocation_id()).orElse(null);
            if (location != null && location.getPoint_id() != null) {
                locationPointRepository.deleteById(location.getPoint_id());
            }
            locationRepository.deleteById(task.getLocation_id());
        }

        if (task.getDeadline_id() != null) {
            reminderRepository.deleteById(task.getDeadline_id());
        }

        taskRepository.deleteById(id);
        log.info("Deleted task with ID: {}", id);

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
                .linkedTaskIds(task.getLinkedTask())
                .build();
    }
}
