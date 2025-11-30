package ru.tcai.taskservice.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TaskRequest {
    private String title;

    private String description;

    private LocationRequest location;

    private DeadlineRequest deadline;

    private Long authorId;

    private Long groupId;

    private Long doerId;

    private String priority;
}
