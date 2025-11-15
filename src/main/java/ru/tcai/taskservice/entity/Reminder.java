package ru.tcai.taskservice.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Embeddable
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "reminder")
public class Reminder {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "time")
    private String time;

    @Column(name = "remindByTime")
    private Boolean remindByTime;
}
