package kz.aitu.builder.car;

/** Dependency-free test runner so the project can be checked with only JDK 17. */
public final class CarBuilderTest {
    private static int passedTests;

    private CarBuilderTest() {
    }

    public static void main(String[] args) {
        run("Director builds a passenger car", CarBuilderTest::directorBuildsPassengerCar);
        run("Director builds a sports car", CarBuilderTest::directorBuildsSportsCar);
        run("Product feature list is immutable", CarBuilderTest::featureListIsImmutable);
        run("Missing required state is rejected", CarBuilderTest::missingStateIsRejected);
        run("Invalid passenger seat count is rejected", CarBuilderTest::invalidPassengerSeatsAreRejected);
        run("Underpowered sports car is rejected", CarBuilderTest::underpoweredSportsCarIsRejected);
        run("Builder resets after a successful build", CarBuilderTest::builderResetsAfterBuild);

        System.out.println("All " + passedTests + " tests passed.");
    }

    private static void directorBuildsPassengerCar() {
        Car car = new CarDirector().constructFamilyCar(new PassengerCarBuilder());

        assertEquals(CarType.PASSENGER, car.getType());
        assertEquals(5, car.getSeats());
        assertEquals(Transmission.AUTOMATIC, car.getTransmission());
    }

    private static void directorBuildsSportsCar() {
        Car car = new CarDirector().constructSportsCar(new SportsCarBuilder());

        assertEquals(CarType.SPORTS, car.getType());
        assertEquals(2, car.getSeats());
        assertTrue(car.getEngine().horsepower() >= 300, "Sports engine should meet the power rule");
    }

    private static void featureListIsImmutable() {
        Car car = new CarDirector().constructFamilyCar(new PassengerCarBuilder());

        assertThrows(UnsupportedOperationException.class, () -> car.getFeatures().add("Unexpected change"));
    }

    private static void missingStateIsRejected() {
        CarBuilder builder = new PassengerCarBuilder();

        assertThrows(IllegalStateException.class, builder::build);
    }

    private static void invalidPassengerSeatsAreRejected() {
        CarBuilder builder = new PassengerCarBuilder()
                .setModel("Too Small")
                .setEngine(new Engine("Test engine", 150, FuelType.HYBRID))
                .setSeats(2)
                .setTransmission(Transmission.AUTOMATIC)
                .setColor("Gray");

        assertThrows(IllegalStateException.class, builder::build);
    }

    private static void underpoweredSportsCarIsRejected() {
        CarBuilder builder = new SportsCarBuilder()
                .setModel("Not Sporty Enough")
                .setEngine(new Engine("Small engine", 120, FuelType.GASOLINE))
                .setSeats(2)
                .setTransmission(Transmission.MANUAL)
                .setColor("Black");

        assertThrows(IllegalStateException.class, builder::build);
    }

    private static void builderResetsAfterBuild() {
        PassengerCarBuilder builder = new PassengerCarBuilder();
        new CarDirector().constructFamilyCar(builder);

        assertThrows(IllegalStateException.class, builder::build);
    }

    private static void run(String testName, Runnable test) {
        try {
            test.run();
            passedTests++;
            System.out.println("PASS: " + testName);
        } catch (RuntimeException | AssertionError error) {
            System.err.println("FAIL: " + testName);
            throw error;
        }
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    private static void assertEquals(Object expected, Object actual) {
        if (!expected.equals(actual)) {
            throw new AssertionError("Expected " + expected + " but got " + actual);
        }
    }

    private static void assertThrows(Class<? extends Throwable> expectedType, Runnable action) {
        try {
            action.run();
        } catch (Throwable error) {
            if (expectedType.isInstance(error)) {
                return;
            }
            throw new AssertionError("Expected " + expectedType.getSimpleName()
                    + " but got " + error.getClass().getSimpleName(), error);
        }
        throw new AssertionError("Expected " + expectedType.getSimpleName() + " but no exception was thrown");
    }
}

