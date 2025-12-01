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
public class NoteDetailsResponse {
    private Long id;
    private String title;
    private String description;
    private LocationResponse location;
    private Long authorId;
    private Long groupId;
    private LocalDateTime createdAt;
    private List<CommentResponse> comments;
}
