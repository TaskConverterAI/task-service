package ru.tcai.taskservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.tcai.taskservice.entity.Comment;
import ru.tcai.taskservice.entity.LinkedTask;

import java.util.List;

@Repository
public interface CommentRepository extends JpaRepository<Comment, Long>  {
    List<Comment> findByTaskId(Long taskId);
}
