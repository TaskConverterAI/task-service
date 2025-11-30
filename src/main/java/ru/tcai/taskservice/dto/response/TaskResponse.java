package ru.tcai.taskservice.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import ru.tcai.taskservice.dto.request.DeadlineRequest;
import ru.tcai.taskservice.dto.request.LocationRequest;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TaskResponse {
    private Long id;
    private String title;
    private String description;
    private Long taskType;
    private LocationRequest location;
    private DeadlineRequest deadline;
    private Long authorId;
    private Long groupId;
    private Long doerId;
    private LocalDateTime createdAt;
    private String priority;
    private String status;
}
