package ru.tcai.taskservice.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Entity
@Embeddable
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "tasks")
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

    @Embedded
    @Column(name = "deadline_id")
    private Long deadline_id;

    @Column(name = "author")
    private Long authorId;

    @Column(name = "groupId")
    private Long groupId;

    @Column(name = "doer")
    private Long doerId;

    @Embedded
    @Column(name = "linkedTask")
    private List<Long> linkedTask;
}
