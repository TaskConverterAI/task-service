package ru.tcai.taskservice.repository;

import ru.tcai.taskservice.entity.LinkedTask;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LinkedTaskRepository extends JpaRepository<LinkedTask, Long> {
    List<LinkedTask> findByTaskId(Long taskId);

    void deleteByTaskId(Long taskId);
}