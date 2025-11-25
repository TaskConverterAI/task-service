package ru.tcai.taskservice.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Embeddable
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "task")
public class Task {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "title")
    private String title;

    @Column(name = "description")
    private String description;

    @Column(name = "taskType")
    private Long taskType;

    @Column(name = "location_id")
    private Long location_id;

    @Column(name = "deadline_id")
    private Long deadline_id;

    @Column(name = "author")
    private Long authorId;

    @Column(name = "groupId")
    private Long groupId;

    @Column(name = "doer")
    private Long doerId;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Column(name = "status")
    private String status;
}
