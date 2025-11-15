package ru.tcai.taskservice.repository;

import ru.tcai.taskservice.entity.LocationPoint;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LocationPointRepository extends JpaRepository<LocationPoint, Long> {
}
