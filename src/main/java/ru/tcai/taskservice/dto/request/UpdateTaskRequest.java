package ru.tcai.taskservice.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UpdateTaskRequest {
    private String title;
    private String description;
    private Long taskType;
    private LocationRequest location;
    private DeadlineRequest deadline;
    private Long groupId;
    private Long doerId;
    private String priority;
    private String status;
}
