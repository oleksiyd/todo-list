# To-Do List Portal

### General Information
This portal runs on ```Flask```, a Python micro web framework. This framework is a good choice for this demo application because:
- It is lightweight and fast
- Provides good tooling and documentation
- Is easy to deploy and test

In development mode the portal runs on ```Werkzeug``` development server, supporting automatic restart on code updates, interactive debugger, detailed error pages, etc. In production mode the portal runs on ```Gunicorn``` (Green Unicorn) Python WSGI HTTP Server.

### Features
- Python ```Flask``` MVC architecture.
- Supports To-Do item CRUD operations with pending/completed status.
- The items list can be refined based on the item status: ```All/Pending/Completed```.
- Supports sorting based on ```Created date, Due date, Title```.
- Runs in Python virtual environment to not contaminate the local dev environment with project dependencies.
- Uses ```Makefile``` to automate frequent local operations.
- Provides a ```Dockerfile``` and is ready to be deployed as a Docker container.
- Uses ```docker compose``` to automate running in a Docker container locally.
- Provides ```integration tests``` to test the portal operations.
- Data persists between application runs. It is stored as a ```JSON``` object in a local file ```./data/todos.json```.

### Trade-offs due to Time Constraints
- The application stores data in a local ```.json``` file, while a production application is expected to store the data in a database.
- No unit tests were implemented.
- The list lacks paginaiton.
- The front-end funcionality relies on ```HTML5``` only without using ```JavaScript/Ajax```.
- The front-end design is rudimentary and not mobile responsive.

## How to Run the Application on MacOS / Linux

### Run Locally in Development Mode
Run the following command to start the application in virtual environment on ```Werkzeug``` server in development mode with enabled automatic restarts on code changes and detailed error information.
```
make run
```
Open (dev server): http://127.0.0.1:5000/

### Run Locally on WSGI Server (production-like)
Run the following command to start the application in virtual environment on ```Gunicorn``` server in production mode.
```
make wsgi
```
Open (dev server): http://127.0.0.1:8000/

### Run Locally as a Docker Container (production-like)
Run the following command to start the application in virtual environment on ```Gunicorn``` server in production mode. This requires locally installed Docker environment, like Docker Desktop.
```
docker compose up --build
```
Open (dev server): http://127.0.0.1:8000/

### How to Run Tests
Run the following command to execute the integration tests.
```
make test
```

### Common Commands (Make)
Run the following command to get the list of all available make commands.
```
make help
```

## Quick Notes about Cloud Infrastructure Design
There are at least two potential scenarios of how the project can be hosted on a cloud computing platform like AWS: 
- Minimum budget scenario
  The portal isn't expected to get frequent updates and a limited number of users will access it. 
- Large Project with Extended Budget Scenario
  The portal is expected to regularly add more services and have a large number of users globally.

### Minimum budget scenario

**Cloud Infrastructure**
- Presentation and business logic layers
  Because the solution isn't expected to add new services and be offered to a large number of users, it can stay monolithic and be hosted in ```AWS ECS Fargate``` as a Docker container. For high availability it will be hosted in at least 2 availability zones and load balanced by ```AWS Application Load Balancer```. There is a need to integrate with ```AWS CloudFront``` and ```WAF``` to be able to cache and serve static content closer to the user and prevent potential attacks.
- Database layer
  The data format is structured, so it can be stored in a relational database, like ```AWS RDS MySQL``` or ```PostgreSQL``` with support for multiple availability zones for high availability.
- DevOps
  The AWS account structure must follow the solution's development cycle and at least have dedicated ```Dev, Test, Prod``` accounts. A merge into the GitHub repository will trigger CI/CD automation implemented as ```AWS CodePipeline``` or ```GitHub workflow```.

### Large Project with Extended Budget Scenario
A large project is expected to steadily add new services and have a large number of clients using it globally. It must be ready for expansion without a need to re-architect existing services. An outage affecting a whole AWS region is a business risk. The following updates will need to be made:
- The solution will need to be re-architected from monolithic design to micro-service architecture.
- The presentation layer (front-end) will need to be hosted separately and be fronted by ```AWS CloudFront``` and ```WAF``` to be able to cache and serve static content closer to the user and prevent potential attacks.

**Cloud Infrastructure**
- In addition to the primary AWS region, the solution must be replicated into the ```Disaster Recovery``` region to be able to recover from region-wide outages in the primary region with minimum downtime and run from the DR region.
- The AWS account structure must be created based on [Domain Driven Design](https://www.geeksforgeeks.org/system-design/domain-driven-design-ddd/) principles
  Parts of the solution must be deployed into their specific domains (bounded context). For example, the presentation layer, the billing services and the ToDo service business workloads will be deployed into separate domains. ```AWS Landing Zone``` can be used to create the multi-account architecture.
- From monolithic architecture, the solution must be broken into separate microservices hosted on ```AWS ECS Fargate```. The east-west traffic including cross-account will be managed by ```AWS ECS Service Connect```. The north-south traffic will be managed by the ```Application Load Balancer```.
- Database layer
  The data format is structured, so it can be stored in a relational database. ```AWS Aurora MySQL``` or ```AWS Aurora PostgreSQL``` with support for high availability, support for multiple master and read-only nodes and cross-region replication must be used for this solution. Alternatively, the data can be stored in JSON format in ```AWS DynamoDB```.
- Networking layer
  ```AWS Transit Gateway``` must be used to enable cross-account network communication.