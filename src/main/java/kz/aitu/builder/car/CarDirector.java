package kz.aitu.builder.car;

import java.util.Objects;

/** Creates reusable car configurations by calling Builder steps in order. */
public final class CarDirector {
    private static final String FAMILY_MODEL = "AITU Family One";
    private static final String SPORTS_MODEL = "AITU Velocity";
    private static final int FAMILY_HORSEPOWER = 180;
    private static final int SPORTS_HORSEPOWER = 450;
    private static final int FAMILY_SEATS = 5;
    private static final int SPORTS_SEATS = 2;

    public Car constructFamilyCar(CarBuilder builder) {
        Objects.requireNonNull(builder, "Builder must not be null");

        return builder.reset()
                .setModel(FAMILY_MODEL)
                .setEngine(new Engine("Efficient Hybrid", FAMILY_HORSEPOWER, FuelType.HYBRID))
                .setSeats(FAMILY_SEATS)
                .setTransmission(Transmission.AUTOMATIC)
                .setColor("Deep Blue")
                .addFeature("Adaptive cruise control")
                .addFeature("Child safety package")
                .addFeature("Large luggage compartment")
                .build();
    }

    public Car constructSportsCar(CarBuilder builder) {
        Objects.requireNonNull(builder, "Builder must not be null");

        return builder.reset()
                .setModel(SPORTS_MODEL)
                .setEngine(new Engine("Twin Turbo V6", SPORTS_HORSEPOWER, FuelType.GASOLINE))
                .setSeats(SPORTS_SEATS)
                .setTransmission(Transmission.DUAL_CLUTCH)
                .setColor("Racing Red")
                .addFeature("Launch control")
                .addFeature("Sport suspension")
                .addFeature("Performance brakes")
                .build();
    }
}

