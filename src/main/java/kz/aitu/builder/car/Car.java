package kz.aitu.builder.car;

import java.util.List;

/** The product created by the builders. */
public class Car {
    private final String type;
    private final String model;
    private final String engine;
    private final int horsepower;
    private final int seats;
    private final String transmission;
    private final String color;
    private final List<String> features;

    Car(String type, String model, String engine, int horsepower, int seats,
        String transmission, String color, List<String> features) {
        this.type = type;
        this.model = model;
        this.engine = engine;
        this.horsepower = horsepower;
        this.seats = seats;
        this.transmission = transmission;
        this.color = color;
        this.features = List.copyOf(features);
    }

    @Override
    public String toString() {
        return "Car{" +
                "type='" + type + '\'' +
                ", model='" + model + '\'' +
                ", engine='" + engine + '\'' +
                ", horsepower=" + horsepower +
                ", seats=" + seats +
                ", transmission='" + transmission + '\'' +
                ", color='" + color + '\'' +
                ", features=" + features +
                '}';
    }
}

