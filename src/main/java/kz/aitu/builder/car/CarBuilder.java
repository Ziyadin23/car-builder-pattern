package kz.aitu.builder.car;

import java.util.ArrayList;
import java.util.List;

/** Builder base class containing the common construction steps. */
public abstract class CarBuilder {
    protected String model;
    protected String engine;
    protected int horsepower;
    protected int seats;
    protected String transmission;
    protected String color;
    protected final List<String> features = new ArrayList<>();

    public CarBuilder setModel(String model) {
        this.model = model;
        return this;
    }

    public CarBuilder setEngine(String engine, int horsepower) {
        this.engine = engine;
        this.horsepower = horsepower;
        return this;
    }

    public CarBuilder setSeats(int seats) {
        this.seats = seats;
        return this;
    }

    public CarBuilder setTransmission(String transmission) {
        this.transmission = transmission;
        return this;
    }

    public CarBuilder setColor(String color) {
        this.color = color;
        return this;
    }

    public CarBuilder addFeature(String feature) {
        features.add(feature);
        return this;
    }

    public Car build() {
        validateCommonFields();
        validateSpecificRules();
        return new Car(getCarType(), model, engine, horsepower, seats,
                transmission, color, features);
    }

    protected abstract String getCarType();

    protected abstract void validateSpecificRules();

    private void validateCommonFields() {
        if (model == null || model.isBlank()) {
            throw new IllegalStateException("Model is required");
        }
        if (engine == null || engine.isBlank()) {
            throw new IllegalStateException("Engine is required");
        }
        if (horsepower <= 0 || seats <= 0) {
            throw new IllegalStateException("Horsepower and seats must be positive");
        }
        if (transmission == null || color == null) {
            throw new IllegalStateException("Transmission and color are required");
        }
    }
}

