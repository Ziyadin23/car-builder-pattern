package kz.aitu.builder.car;

/** Contains reusable sequences for building common car configurations. */
public class CarDirector {

    public Car buildFamilyCar(CarBuilder builder) {
        return builder
                .setModel("Toyota Camry")
                .setEngine("2.5L Hybrid", 218)
                .setSeats(5)
                .setTransmission("Automatic")
                .setColor("White")
                .addFeature("Air conditioning")
                .addFeature("Parking camera")
                .build();
    }

    public Car buildSportsCar(CarBuilder builder) {
        return builder
                .setModel("Nissan GT-R")
                .setEngine("3.8L Twin Turbo", 565)
                .setSeats(2)
                .setTransmission("Dual clutch")
                .setColor("Red")
                .addFeature("Sport suspension")
                .addFeature("Launch control")
                .build();
    }
}

