package kz.aitu.builder.car;

import java.util.List;
import java.util.Objects;

/**
 * The immutable product created by the builders.
 * A defensive copy prevents callers from changing the feature list afterward.
 */
public final class Car {
    private final String model;
    private final CarType type;
    private final Engine engine;
    private final int seats;
    private final Transmission transmission;
    private final String color;
    private final List<String> features;

    Car(
            String model,
            CarType type,
            Engine engine,
            int seats,
            Transmission transmission,
            String color,
            List<String> features
    ) {
        this.model = model;
        this.type = Objects.requireNonNull(type);
        this.engine = Objects.requireNonNull(engine);
        this.seats = seats;
        this.transmission = Objects.requireNonNull(transmission);
        this.color = color;
        this.features = List.copyOf(features);
    }

    public String getModel() {
        return model;
    }

    public CarType getType() {
        return type;
    }

    public Engine getEngine() {
        return engine;
    }

    public int getSeats() {
        return seats;
    }

    public Transmission getTransmission() {
        return transmission;
    }

    public String getColor() {
        return color;
    }

    public List<String> getFeatures() {
        return features;
    }

    @Override
    public String toString() {
        return "Car{" +
                "model='" + model + '\'' +
                ", type=" + type +
                ", engine=" + engine.name() + " (" + engine.horsepower() + " hp, " + engine.fuelType() + ")" +
                ", seats=" + seats +
                ", transmission=" + transmission +
                ", color='" + color + '\'' +
                ", features=" + features +
                '}';
    }
}

