package kz.aitu.builder.car;

import java.util.Objects;

/** Immutable engine specification used as part of a {@link Car}. */
public record Engine(String name, int horsepower, FuelType fuelType) {

    public Engine {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Engine name must not be blank");
        }
        if (horsepower <= 0) {
            throw new IllegalArgumentException("Horsepower must be greater than zero");
        }
        Objects.requireNonNull(fuelType, "Fuel type must not be null");
    }
}
