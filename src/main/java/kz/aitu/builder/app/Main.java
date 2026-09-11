package kz.aitu.builder.app;

import kz.aitu.builder.car.Car;
import kz.aitu.builder.car.CarDirector;
import kz.aitu.builder.car.PassengerCarBuilder;
import kz.aitu.builder.car.SportsCarBuilder;

/** Client class that demonstrates the Builder pattern. */
public class Main {
    public static void main(String[] args) {
        CarDirector director = new CarDirector();

        Car familyCar = director.buildFamilyCar(new PassengerCarBuilder());
        Car sportsCar = director.buildSportsCar(new SportsCarBuilder());

        System.out.println("Family car:");
        System.out.println(familyCar);

        System.out.println("\nSports car:");
        System.out.println(sportsCar);
    }
}
