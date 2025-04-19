This is the approach for file organization and division of tasks:

```
Blueprints
    └── Services
        ├── Model (dataclass)
        ├── Helpers (Gateways like Sendgrid and Paypal)
        └── Repositories
             └── Database
```

- Blueprints: These are the entry points to the API. Blueprints call Services and raise http exceptions if there is an underlying exception. Blueprints hide implementation details, including error message details, from the client.
- Services: These are the orchestrators. They call the Models, Gateways and Repositories to perform the business logic.
- Helpers: These refer to Gateways to other services. Their implementation is abstracted in separate classes so that updates to the Gateways is isolated from the rest of the application logic.
- Models: Models represent objects in the system. For example, Users and Products. Most of the logic here is to make operations within the object itself. In other words, the object is unaware of the business logic of the application.
- Repositories: They communicate with the Database. Any operation with the database has to go through the Repositories for validation, transformation and sanitization.

Some comments and possible TODOs:
- Maybe we should separate the Helpers directory in Gateways and Helpers
- TODO: Convert some Service methods to be static/class methods

How to install the dependencies:
```bash
poetry install
```

How to run the tests:
```bash
pytest
```

How to start the service locally (run from the root directory):
```bash
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```
