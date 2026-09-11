package kz.aitu.builder.car;

/** Builds practical passenger cars with four to seven seats. */
public final class PassengerCarBuilder extends AbstractCarBuilder {
    private static final int MINIMUM_PASSENGER_SEATS = 4;
    private static final int MAXIMUM_PASSENGER_SEATS = 7;

    public PassengerCarBuilder() {
        super(CarType.PASSENGER);
    }

    @Override
    protected void validateSpecificState() {
        if (seats < MINIMUM_PASSENGER_SEATS || seats > MAXIMUM_PASSENGER_SEATS) {
            throw new IllegalStateException(
                    "Passenger car seat count must be between "
                            + MINIMUM_PASSENGER_SEATS + " and " + MAXIMUM_PASSENGER_SEATS
            );
        }
    }
}

