package ru.tcai.taskservice.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LocationRequest {
    private Double latitude;
    private Double longitude;
    private String name;
    private Boolean remindByLocation;
}
