package kz.aitu.builder.car;

/**
 * Builder abstraction that declares every step available to the Director and Client.
 * Returning CarBuilder from each configuration method enables a fluent API.
 */
public interface CarBuilder {
    CarBuilder reset();

    CarBuilder setModel(String model);

    CarBuilder setEngine(Engine engine);

    CarBuilder setSeats(int seats);

    CarBuilder setTransmission(Transmission transmission);

    CarBuilder setColor(String color);

    CarBuilder addFeature(String feature);

    Car build();
}

