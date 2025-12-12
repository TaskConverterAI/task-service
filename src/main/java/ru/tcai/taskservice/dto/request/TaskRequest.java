package ru.tcai.taskservice.dto.request;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import jakarta.validation.constraints.NotBlank;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TaskRequest {
    @NotBlank
    @NotNull
    @Size(min = 1, max = 255)
    private String title;

    @NotNull
    @Size(min = 0, max = 255)
    private String description;

    @Valid
    private LocationRequest location;

    @Valid
    private DeadlineRequest deadline;

    @NotNull
    private Long authorId;

    private Long groupId;

    private Long doerId;

    @Pattern(regexp = "LOW|MIDDLE|HIGH", message = "priority must be LOW, MIDDLE or HIGH")
    private String priority;

    @Pattern(regexp = "UNDONE|DONE", message = "status must be DONE or UNDONE")
    private String status;
}
