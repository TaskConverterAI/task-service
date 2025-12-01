package ru.tcai.taskservice.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NoteRequest {
    private String title;

    private String description;

    private LocationRequest location;

    private Long authorId;

    private Long groupId;
}
