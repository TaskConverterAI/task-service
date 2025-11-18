package ru.tcai.taskservice.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SubtaskResponse {
    private Long id;
    private String description;
    private Long authorId;
    private Long groupId;
    private Long doerId;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private String status;
}
