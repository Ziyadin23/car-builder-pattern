package kz.aitu.builder.car;

/** Builds normal passenger cars. */
public class PassengerCarBuilder extends CarBuilder {
    private static final int MIN_SEATS = 4;
    private static final int MAX_SEATS = 7;

    @Override
    protected String getCarType() {
        return "Passenger Car";
    }

    @Override
    protected void validateSpecificRules() {
        if (seats < MIN_SEATS || seats > MAX_SEATS) {
            throw new IllegalStateException("A passenger car must have 4 to 7 seats");
        }
    }
}

