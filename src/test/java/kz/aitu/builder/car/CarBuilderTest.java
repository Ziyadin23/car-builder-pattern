package kz.aitu.builder.car;

/** Small test class that does not require an external testing library. */
public class CarBuilderTest {
    private static int passedTests = 0;

    public static void main(String[] args) {
        testPassengerCarIsBuilt();
        testSportsCarIsBuilt();
        testPassengerSeatValidation();
        testSportsHorsepowerValidation();

        System.out.println("All " + passedTests + " tests passed.");
    }

    private static void testPassengerCarIsBuilt() {
        Car car = new CarDirector().buildFamilyCar(new PassengerCarBuilder());

        check(car.toString().contains("type='Passenger Car'"),
                "The family car should be a passenger car");
    }

    private static void testSportsCarIsBuilt() {
        Car car = new CarDirector().buildSportsCar(new SportsCarBuilder());

        check(car.toString().contains("type='Sports Car'"),
                "The sports configuration should create a sports car");
    }

    private static void testPassengerSeatValidation() {
        expectInvalidCar(
                () -> new PassengerCarBuilder()
                        .setModel("Test car")
                        .setEngine("Test engine", 150)
                        .setSeats(2)
                        .setTransmission("Automatic")
                        .setColor("Black")
                        .build(),
                "Passenger builder should reject a two-seat car");
    }

    private static void testSportsHorsepowerValidation() {
        expectInvalidCar(
                () -> new SportsCarBuilder()
                        .setModel("Test car")
                        .setEngine("Test engine", 200)
                        .setSeats(2)
                        .setTransmission("Manual")
                        .setColor("Red")
                        .build(),
                "Sports builder should reject an underpowered car");
    }

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
        passedTests++;
    }

    private static void expectInvalidCar(Runnable action, String message) {
        try {
            action.run();
            throw new AssertionError(message);
        } catch (IllegalStateException expected) {
            passedTests++;
        }
    }
}
