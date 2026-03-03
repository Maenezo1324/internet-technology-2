# Диаграмма классов платформы стажировок DOKE

```mermaid
classDiagram
    class User {
        +int id
        +String name
        +String email
    }
    class Trainee {
        +float averageScore
        +completeTask()
    }
    class Intern {
        +Project currentProject
        +workOnProject()
    }
    class Teacher {
        +gradeTask()
        +createCourse()
    }
    class Direction {
        <<enumeration>>
        iOS
        Android
        Backend
    }
    class Course {
        +String title
        +Direction direction
    }
    class Internship {
        +Date startDate
        +Date endDate
        +enrollTrainee()
    }
    class Task {
        +String description
        +int maxScore
    }
    class Grade {
        +int score
        +String feedback
    }

    User <|-- Trainee
    User <|-- Intern
    User <|-- Teacher
    
    Internship "1" *-- "many" Course
    Course "1" *-- "many" Task
    Task "1" o-- "many" Grade
    Trainee "1" o-- "many" Grade
    Course --> Direction