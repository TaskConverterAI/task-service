package ru.tcai.taskservice.dto.request;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LocationRequest {
    @NotNull @Min(-90) @Max(90)
    private Double latitude;
    @NotNull @Min(-180) @Max(180)
    private Double longitude;
    @NotNull @Size(min=0, max=255)
    private String name;
    private Boolean remindByLocation;
}
