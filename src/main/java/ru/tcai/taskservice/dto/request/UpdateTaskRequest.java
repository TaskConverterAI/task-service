package ru.tcai.taskservice.dto.request;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UpdateTaskRequest {
    @Size(min = 1, max = 255)
    private String title;
    @Size(max = 255)
    private String description;
    private Long taskType;
    @Valid
    private LocationRequest location;
    @Valid
    private DeadlineRequest deadline;
    private Long groupId;
    private Long doerId;
    @Pattern(regexp="LOW|MIDDLE|HIGH", message = "priority must be LOW, MIDDLE or HIGH")
    private String priority;
    @Pattern(regexp="DONE|UNDONE", message = "status must be DONE or UNDONE")
    private String status;
}
