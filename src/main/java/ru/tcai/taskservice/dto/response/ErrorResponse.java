package ru.tcai.taskservice.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Value;

import java.time.LocalDateTime;

@Value
@Builder
public class ErrorResponse {
    @JsonInclude(JsonInclude.Include.NON_NULL)
    LocalDateTime timestamp;

    @JsonInclude(JsonInclude.Include.NON_NULL)
    Integer status;

    @JsonInclude(JsonInclude.Include.NON_NULL)
    String message;
}
