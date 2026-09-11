# Car Builder Pattern Defense Guide

This guide explains the project from the beginning and gives you a practical script for the in-class defense. Read the source code while using the guide. The instructor may ask you to change or explain any part of the program.

## 1. Basic Java terms used in this project

### Class

A class is a definition of a type of object. It describes the data an object contains and the operations it can perform. `Car` is a class. Each finished car created by the program is an object of that class.

### Object

An object is one concrete instance of a class. In this statement, `familyCar` refers to a new `Car` object:

```java
Car familyCar = director.constructFamilyCar(new PassengerCarBuilder());
```

### Field

A field is a value stored inside an object. `Car` has fields such as `model`, `engine`, `seats`, and `color`.

### Method

A method is a named operation. For example, `setSeats(5)` stores a seat count in the builder, and `build()` validates the values and creates the finished car.

### Constructor

A constructor initializes a new object. Its name matches the class name. This creates a new builder:

```java
new PassengerCarBuilder()
```

The `Car` constructor is package-private, so normal client code in another package cannot bypass the builders easily.

### Interface

An interface is a contract. It declares methods without storing the complete implementation. `CarBuilder` says that every car builder must support methods such as `setEngine()`, `setSeats()`, and `build()`.

The Director depends on `CarBuilder`, not on one concrete builder. This is useful because the Director can call the same construction steps on different implementations.

### Abstract class

An abstract class is a partially implemented base class that cannot be instantiated directly. `AbstractCarBuilder` implements behavior shared by both concrete builders. It stores temporary construction state, implements the fluent setters, performs common validation, and creates the final product.

### Inheritance

Inheritance allows one class to reuse and specialize another class. `PassengerCarBuilder` and `SportsCarBuilder` extend `AbstractCarBuilder`. They inherit common behavior and implement only their specific validation rules.

### Polymorphism

Polymorphism means code can work through a common type while the actual object may have different implementations. A variable of type `CarBuilder` can refer to either a `PassengerCarBuilder` or a `SportsCarBuilder`.

### Enum

An enum defines a fixed set of named values. `FuelType` can only be `GASOLINE`, `ELECTRIC`, or `HYBRID`. Enums prevent inconsistent text values such as `"gas"`, `"Gasoline"`, and `"petrol"` from representing the same concept.

### Record

A Java record is a compact way to define a value object. `Engine` is a record containing `name`, `horsepower`, and `fuelType`. Its compact constructor validates these values.

### Exception

An exception reports a problem that prevents normal execution. `build()` throws `IllegalStateException` when required construction state is missing or inconsistent. For example, the sports builder rejects an engine below 300 horsepower.

### Immutable object

An immutable object cannot change after construction. Every `Car` field is `final`, the class exposes no setters, and `List.copyOf(features)` protects the feature list. Immutability makes a completed product safe to share because later builder operations cannot change it.

## 2. What problem the Builder pattern solves

Without Builder, a client might need a constructor like this:

```java
new Car("AITU Velocity", CarType.SPORTS, engine, 2,
        Transmission.DUAL_CLUTCH, "Racing Red", features);
```

This constructor works, but several arguments are difficult to identify without reading the constructor definition. Multiple optional values can also lead to many overloaded constructors.

Builder replaces that call with named steps:

```java
new SportsCarBuilder()
        .setModel("AITU Velocity")
        .setEngine(engine)
        .setSeats(2)
        .setTransmission(Transmission.DUAL_CLUTCH)
        .setColor("Racing Red")
        .build();
```

The result is easier to read, optional steps are easy to add, and validation remains inside the builder.

## 3. Pattern roles in this project

### Product

`Car` is the Product. It is the completed object returned by `build()`.

### Builder

`CarBuilder` is the Builder interface. It declares the construction steps shared by every representation.

### Concrete Builders

`PassengerCarBuilder` and `SportsCarBuilder` are the Concrete Builders. They produce the same Product class but attach different `CarType` values and enforce different rules.

The passenger representation requires four to seven seats. The sports representation permits no more than two seats, requires at least 300 horsepower, and rejects a normal automatic transmission. These are meaningful behavioral differences, not merely different class names.

### Director

`CarDirector` stores reusable recipes. `constructFamilyCar()` and `constructSportsCar()` call the same Builder operations in known sequences. The Director is optional because the client can also use a builder directly.

### Client

`Main` is the Client. It chooses concrete builders, asks the Director to run recipes, constructs one custom car directly, and prints the products.

## 4. What happens during one build

Consider the family car:

1. `Main` creates `PassengerCarBuilder`.
2. `Main` passes it to `CarDirector.constructFamilyCar()`.
3. The Director calls `reset()` to clear old temporary state.
4. The Director calls the fluent setters for model, engine, seats, transmission, color, and features.
5. Each setter returns `this`, which is the current builder. That makes method chaining possible.
6. The Director calls `build()`.
7. `AbstractCarBuilder` validates required values.
8. `PassengerCarBuilder.validateSpecificState()` checks the passenger seat rule.
9. The builder creates a new immutable `Car`.
10. The builder resets its temporary fields and returns the finished car.

The sports build follows the same overall algorithm but executes the sports-specific validation method. This is an example of the Template Method idea inside the Builder implementation: the base class controls the algorithm and subclasses supply one specialized step.

## 5. Why method chaining works

The setter stores a value and returns the same builder:

```java
public final CarBuilder setSeats(int seats) {
    this.seats = seats;
    return this;
}
```

Because the result is another `CarBuilder`, Java allows the next call immediately:

```java
builder.setSeats(5).setColor("Blue").build();
```

This style is called a fluent API. “Fluent” means the sequence reads like a description of the object being built.

## 6. Why there are two levels of validation

`validateCommonState()` checks rules that apply to every car: model, engine, seat count, transmission, and color must be present and valid.

`validateSpecificState()` checks rules that depend on the representation. This separation prevents duplicate common checks and keeps passenger rules out of the sports builder.

The order matters. Common validation checks that `engine` is present before the sports builder calls `engine.horsepower()`. Otherwise, an absent engine could cause a less helpful `NullPointerException`.

## 7. Clean Code points to explain

Be ready to show these directly in the code:

1. **Meaningful names:** `constructFamilyCar`, `MINIMUM_SPORTS_HORSEPOWER`, and `validateSpecificState` describe their purposes.
2. **Small focused units:** `Main` demonstrates, `CarDirector` stores recipes, `Car` stores the product, and builders construct it.
3. **No duplicated builder logic:** `AbstractCarBuilder` contains setters, common validation, construction, and reset behavior once.
4. **Validated construction:** invalid configurations throw clear exceptions before a Product is created.
5. **No magic numbers:** values such as the 300 hp threshold have named constants.
6. **Immutability:** final fields and defensive list copying protect the completed Product.
7. **Purposeful comments:** class comments explain design intent; obvious statements are left to readable code.

## 8. Tests and what they prove

Run:

```bash
./scripts/test.sh
```

The seven tests cover successful passenger and sports builds, immutability, missing state, invalid passenger seats, insufficient sports-car power, and automatic reset after a successful build.

These tests include positive cases and negative cases. A positive test proves a valid configuration succeeds. A negative test proves an invalid configuration fails in the intended way.

## 9. Git and GitHub basics

Git is the version-control program that records the history of files locally. GitHub hosts a Git repository online so it can be shared.

A commit is a named snapshot of a meaningful stage. This repository has separate commits for project setup, the Product and builders, the Director and Client, tests, documentation, and the report. This satisfies the requirement for incremental history better than one “final” commit.

Useful commands:

```bash
git status
git log --oneline
git remote -v
```

- `git status` shows changed or untracked files.
- `git log --oneline` shows the incremental commit history.
- `git remote -v` shows the connected GitHub repository.

## 10. Suggested defense demonstration

1. Open the UML diagram and identify Product, Builder, Concrete Builders, Director, and Client.
2. Open `CarBuilder.java` and explain that it defines the common construction contract.
3. Open `AbstractCarBuilder.java` and show method chaining, validation, object creation, and reset.
4. Compare `PassengerCarBuilder.java` with `SportsCarBuilder.java`.
5. Open `CarDirector.java` and show the two reusable recipes.
6. Open `Main.java` and point out Director-based and direct builder usage.
7. Run `./scripts/test.sh`.
8. Run `./scripts/run.sh` and compare the printed products.
9. Show `git log --oneline` to demonstrate incremental work.

## 11. Short defense script

You can use this as an outline, but speak naturally and make sure you understand each sentence:

> My Product is an immutable Car containing a model, type, engine, seats, transmission, color, and features. I used Builder because the object has several required and optional values, two meaningful representations, and rules that should be checked before construction. CarBuilder defines the fluent construction steps. AbstractCarBuilder implements shared setters, common validation, creation, and reset behavior. PassengerCarBuilder and SportsCarBuilder add their own domain rules. CarDirector provides reusable family and sports recipes, while Main demonstrates both the Director and direct fluent construction. The tests show that valid cars are created, invalid cars are rejected, and the completed Product cannot be changed.

## 12. Likely questions and answers

### Why not use one large constructor

A large constructor hides the meaning of similar arguments, becomes difficult to change, and handles optional values poorly. Builder uses named steps and performs validation before construction.

### Why is the Director optional

The Builder can construct a product by itself. The Director is valuable only when the program needs known, reusable sequences. The custom electric example proves that clients can bypass the Director.

### Why use an interface and an abstract class

The interface defines the contract visible to the Director and clients. The abstract class reuses implementation without forcing duplicated code into concrete builders.

### How are the two builders meaningfully different

They set different car types and enforce different constraints. Passenger cars require four to seven seats. Sports cars require at most two seats, at least 300 horsepower, and a manual or dual-clutch transmission.

### What happens if build is called too early

Common validation detects the missing value and throws `IllegalStateException` with a clear message. No incomplete Car is returned.

### Why reset after build

The builder contains mutable temporary state. Resetting prevents values from the previous car from leaking into the next build when the same builder is reused.

### What is a disadvantage of this solution

Builder adds several classes and more code. It is useful for this multi-part Product, but it would be excessive for a very simple object with only a few values.

### Could the Director receive the wrong builder

Yes. The common interface allows any CarBuilder to be passed to either recipe. Representation-specific validation rejects an incompatible result at build time. Separate typed Director methods could prevent the mismatch earlier, but they would reduce the uniformity of the interface.

## 13. Before you submit

Replace the student-name and group placeholders in the Word report. Confirm the exact date in Moodle. Run the program and tests yourself, read the report in your own words, and check that you can explain every submitted class. The assignment states that the report and code must be your own, so personalize the conclusion if your own experience differs from the supplied draft.

