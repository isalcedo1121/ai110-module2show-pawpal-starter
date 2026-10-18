# PawPal+ UML Draft (Phase 1)

```mermaid
classDiagram
    class Owner {
        +str name
        +list~Pet~ pets
        +add_pet(pet: Pet) None
        +remove_pet(pet: Pet) None
        +get_all_tasks() list~Task~
    }

    class Pet {
        +str name
        +str species
        +int age
        +list~Task~ tasks
        +add_task(task: Task) None
        +remove_task(task: Task) None
    }

    class Task {
        +str name
        +int duration
        +int priority
        +str due_time
        +str frequency
        +bool completed
        +mark_complete() None
    }

    class Scheduler {
        +Owner owner
        +generate_schedule(available_minutes: int) list~Task~
    }

    note for Task "priority: higher number = higher priority\ndue_time: 24-hour HH:MM string"

    Owner "1" o-- "0..*" Pet : owns
    Pet "1" *-- "0..*" Task : has
    Scheduler "1" --> "1" Owner : plans for
```

## Relationships

- **Owner → Pet (aggregation, 1 to many):** An owner keeps a list of pets and can add or remove them. A pet is its own object and still makes sense apart from any particular owner.
- **Pet → Task (composition, 1 to many):** Each pet has its own care tasks (feeding, walks, meds). A task belongs to a single pet and has no meaning without it.
- **Scheduler → Owner (association, 1 to 1):** The scheduler holds a reference to an owner and reads tasks through `owner.get_all_tasks()` (which collects them from `owner.pets`) when `generate_schedule(available_minutes)` builds the daily plan. It keeps no task list of its own, so each pet's `tasks` is the single source of truth.
