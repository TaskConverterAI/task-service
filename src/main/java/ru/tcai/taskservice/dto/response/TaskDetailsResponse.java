package ru.tcai.taskservice.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TaskDetailsResponse {
    private Long id;
    private String title;
    private String description;
    private Long taskType;
    private LocationResponse location;
    private DeadlineResponse deadline;
    private Long authorId;
    private Long groupId;
    private Long doerId;
    private LocalDateTime createdAt;
    private List<SubtaskResponse> subtasks;
}
