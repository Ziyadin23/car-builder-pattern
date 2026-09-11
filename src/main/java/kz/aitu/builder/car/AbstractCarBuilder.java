package kz.aitu.builder.car;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Holds construction state and shared build logic so concrete builders do not
 * duplicate fluent setters or common validation.
 */
public abstract class AbstractCarBuilder implements CarBuilder {
    private static final int MINIMUM_SEAT_COUNT = 1;

    protected String model;
    protected Engine engine;
    protected int seats;
    protected Transmission transmission;
    protected String color;
    protected final List<String> features = new ArrayList<>();

    private final CarType carType;

    protected AbstractCarBuilder(CarType carType) {
        this.carType = Objects.requireNonNull(carType);
        reset();
    }

    @Override
    public final CarBuilder reset() {
        model = null;
        engine = null;
        seats = 0;
        transmission = null;
        color = null;
        features.clear();
        return this;
    }

    @Override
    public final CarBuilder setModel(String model) {
        this.model = normalize(model);
        return this;
    }

    @Override
    public final CarBuilder setEngine(Engine engine) {
        this.engine = engine;
        return this;
    }

    @Override
    public final CarBuilder setSeats(int seats) {
        this.seats = seats;
        return this;
    }

    @Override
    public final CarBuilder setTransmission(Transmission transmission) {
        this.transmission = transmission;
        return this;
    }

    @Override
    public final CarBuilder setColor(String color) {
        this.color = normalize(color);
        return this;
    }

    @Override
    public final CarBuilder addFeature(String feature) {
        String normalizedFeature = normalize(feature);
        if (normalizedFeature == null) {
            throw new IllegalArgumentException("Feature must not be blank");
        }
        if (!features.contains(normalizedFeature)) {
            features.add(normalizedFeature);
        }
        return this;
    }

    @Override
    public final Car build() {
        validateCommonState();
        validateSpecificState();

        Car result = new Car(model, carType, engine, seats, transmission, color, features);
        reset();
        return result;
    }

    protected abstract void validateSpecificState();

    private void validateCommonState() {
        if (model == null) {
            throw new IllegalStateException("Car model must be provided before build()");
        }
        if (engine == null) {
            throw new IllegalStateException("Car engine must be provided before build()");
        }
        if (seats < MINIMUM_SEAT_COUNT) {
            throw new IllegalStateException("Car must have at least one seat");
        }
        if (transmission == null) {
            throw new IllegalStateException("Car transmission must be provided before build()");
        }
        if (color == null) {
            throw new IllegalStateException("Car color must be provided before build()");
        }
    }

    private static String normalize(String value) {
        if (value == null || value.isBlank()) {
            return null;
        }
        return value.trim();
    }
}

