package ru.tcai.taskservice.dto.request;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UpdateNoteRequest {
    @Size(min = 1, max = 255)
    private String title;
    @Size(max = 255)
    private String description;
    @Valid
    private LocationRequest location;
    private Long groupId;
}
