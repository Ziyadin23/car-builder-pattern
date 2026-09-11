package kz.aitu.builder.app;

import kz.aitu.builder.car.Car;
import kz.aitu.builder.car.CarDirector;
import kz.aitu.builder.car.Engine;
import kz.aitu.builder.car.FuelType;
import kz.aitu.builder.car.PassengerCarBuilder;
import kz.aitu.builder.car.SportsCarBuilder;
import kz.aitu.builder.car.Transmission;

/** Client that demonstrates Director-based and direct fluent construction. */
public final class Main {
    private Main() {
    }

    public static void main(String[] args) {
        CarDirector director = new CarDirector();

        Car familyCar = director.constructFamilyCar(new PassengerCarBuilder());
        Car sportsCar = director.constructSportsCar(new SportsCarBuilder());

        Car customPassengerCar = new PassengerCarBuilder()
                .setModel("AITU Eco Custom")
                .setEngine(new Engine("Electric Drive", 220, FuelType.ELECTRIC))
                .setSeats(5)
                .setTransmission(Transmission.AUTOMATIC)
                .setColor("Pearl White")
                .addFeature("Fast charging")
                .addFeature("Heated seats")
                .build();

        printCar("Family configuration from Director", familyCar);
        printCar("Sports configuration from Director", sportsCar);
        printCar("Custom configuration from fluent API", customPassengerCar);
    }

    private static void printCar(String label, Car car) {
        System.out.println(label);
        System.out.println(car);
        System.out.println();
    }
}

