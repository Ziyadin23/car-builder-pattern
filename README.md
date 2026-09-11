# Car Builder Pattern

Assignment 1 for the Software Design Patterns course.

Student: Ziyadinkhan Kudaibergenuly  
Group: SE 2501

## Description

This project demonstrates the Builder design pattern in Java. The product is a `Car`.

The program contains:

- `Car` - the product.
- `CarBuilder` - an abstract builder with the common construction steps.
- `PassengerCarBuilder` - builds passenger cars.
- `SportsCarBuilder` - builds sports cars.
- `CarDirector` - contains ready construction sequences.
- `Main` - runs the example.

The two concrete builders have different rules. A passenger car must have four to seven seats. A sports car can have at most two seats and must have at least 300 horsepower.

## Project structure

```text
src/main/java/kz/aitu/builder/
├── app/Main.java
└── car/
    ├── Car.java
    ├── CarBuilder.java
    ├── CarDirector.java
    ├── PassengerCarBuilder.java
    └── SportsCarBuilder.java
```

## Requirements

- JDK 17

## How to run

Open the project in IntelliJ IDEA and run `Main.java`.

You can also run it from the terminal:

```bash
./scripts/run.sh
```

## Example

```java
Car familyCar = director.buildFamilyCar(new PassengerCarBuilder());
Car sportsCar = director.buildSportsCar(new SportsCarBuilder());
```

Each setter returns the builder itself, so method chaining can be used:

```java
builder.setModel("Toyota Camry")
       .setSeats(5)
       .setColor("White")
       .build();
```

## UML

The UML diagram is located in `docs/uml/car-builder.png`. The PlantUML source is in `docs/uml/car-builder.puml`.

