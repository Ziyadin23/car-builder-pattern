package kz.aitu.builder.car;

/** Builds high-performance sports cars with stricter domain rules. */
public final class SportsCarBuilder extends AbstractCarBuilder {
    private static final int MAXIMUM_SPORTS_SEATS = 2;
    private static final int MINIMUM_SPORTS_HORSEPOWER = 300;

    public SportsCarBuilder() {
        super(CarType.SPORTS);
    }

    @Override
    protected void validateSpecificState() {
        if (seats > MAXIMUM_SPORTS_SEATS) {
            throw new IllegalStateException(
                    "Sports car seat count must not exceed " + MAXIMUM_SPORTS_SEATS
            );
        }
        if (engine.horsepower() < MINIMUM_SPORTS_HORSEPOWER) {
            throw new IllegalStateException(
                    "Sports car engine must produce at least " + MINIMUM_SPORTS_HORSEPOWER + " hp"
            );
        }
        if (transmission == Transmission.AUTOMATIC) {
            throw new IllegalStateException(
                    "Sports car must use MANUAL or DUAL_CLUTCH transmission"
            );
        }
    }
}
