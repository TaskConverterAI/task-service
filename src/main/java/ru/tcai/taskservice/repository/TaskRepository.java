package ru.tcai.taskservice.repository;

import ru.tcai.taskservice.entity.Task;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {
    List<Task> findByAuthorId(Long authorId);

    List<Task> findByGroupId(Long groupId);

    List<Task> findByDoerId(Long doerId);
}
