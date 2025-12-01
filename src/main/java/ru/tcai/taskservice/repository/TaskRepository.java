package ru.tcai.taskservice.repository;

import ru.tcai.taskservice.entity.Task;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {
    List<Task> findByGroupIdIsNullAndAuthorId(Long authorId);

    List<Task> findByGroupIdIsNullAndAuthorIdAndTaskType(Long authorId, Integer taskType);

    List<Task> findByAuthorIdAndTaskType(Long authorId, Integer taskType);

    List<Task> findByGroupIdAndTaskType(Long groupId, Integer taskType);

    List<Task> findByDoerIdAndTaskType(Long doerId, Integer taskType);
}
