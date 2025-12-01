package ru.tcai.taskservice.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import ru.tcai.taskservice.dto.request.LocationRequest;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NoteResponse {
    private Long id;
    private String title;
    private String description;
    private LocationRequest location;
    private Long authorId;
    private Long groupId;
    private LocalDateTime createdAt;
}
