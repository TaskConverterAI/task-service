CREATE TABLE IF NOT EXISTS task
(
    id                 BIGSERIAL PRIMARY KEY,
    author             BIGINT,
    title              VARCHAR(255),
    taskType           BIGINT,
    description        VARCHAR(255)            NOT NULL,
    location_id	       BIGINT,
    deadline_id        BIGINT,
    groupId            BIGINT,
    doer               BIGINT,
    created_at         TIMESTAMP,
    updated_at         TIMESTAMP,
    status             VARCHAR(255),
    priority           VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS comment
(
    id                 BIGSERIAL PRIMARY KEY,
    task_id            BIGINT,
    author_id          BIGINT,
    text               VARCHAR(255),
    created_at         TIMESTAMP
);

CREATE TABLE IF NOT EXISTS location
(
    id                 BIGSERIAL PRIMARY KEY,
    point_id           BIGSERIAL,
    remindByLocation   BOOLEAN
);

CREATE TABLE IF NOT EXISTS location_point
(
   id                  BIGSERIAL PRIMARY KEY,
   latitude            DOUBLE PRECISION,
   longitude           DOUBLE PRECISION,
   name                VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS reminder
(
    id                 BIGSERIAL PRIMARY KEY,
    time               VARCHAR(255),
    remindByTime       BOOLEAN
);

ALTER TABLE location ADD FOREIGN KEY (point_id)    REFERENCES location_point(id);
ALTER TABLE task     ADD FOREIGN KEY (location_id) REFERENCES location(id);
ALTER TABLE task     ADD FOREIGN KEY (deadline_id) REFERENCES reminder(id);

ALTER TABLE comment ADD CONSTRAINT fk_comment_task FOREIGN KEY (task_id) REFERENCES task(id);
