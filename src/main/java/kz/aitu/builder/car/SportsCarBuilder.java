package kz.aitu.builder.car;

/** Builds sports cars with simple performance rules. */
public class SportsCarBuilder extends CarBuilder {
    private static final int MAX_SEATS = 2;
    private static final int MIN_HORSEPOWER = 300;

    @Override
    protected String getCarType() {
        return "Sports Car";
    }

    @Override
    protected void validateSpecificRules() {
        if (seats > MAX_SEATS) {
            throw new IllegalStateException("A sports car cannot have more than 2 seats");
        }
        if (horsepower < MIN_HORSEPOWER) {
            throw new IllegalStateException("A sports car must have at least 300 horsepower");
        }
    }
}

