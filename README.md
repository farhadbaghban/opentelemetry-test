# Django OpenTelemetry Test Repository

This repository is designed to test and implement OpenTelemetry with Django. It contains two Django projects:  

- **test_open**: Handles user authentication.  
- **test_open_order**: Manages `Order` and `OrderItem` models and integrates with `test_open` for user information.
- **test_trip**: Manages `Trip` model and integrates with `test_open` for user information and `test_open_order` for orders.
- **consumer**: Manages the `RequestResponse` model and consumes from services for logging data.  

The repository includes migration files, and it is essential to migrate the database before running the projects.

## Features

1. **User Authentication**:  
   The `test_open` project provides authentication services for the `test_open_order` project.  

2. **Order Management**:  
   The `test_open_order` project includes models for orders and order items, with data tied to authenticated users.

3. **OpenTelemetry Integration**:  
   OpenTelemetry is implemented to trace requests and interactions across the projects.

4. **Trip Management**:  
   The `test_trip` project includes models for Trips, that create trips with some required data and call User and Order services.

3. **Consumer**:  
   The `consumer` project includes models for Request and Response dataLOG and consumes data from a RabbitMQ queue with a django command.

## Requirements

- Python 3.8+  
- Django 4.x  
- Docker (for Jaeger tracing)  
- PostgreSQL (or your preferred database setup)  

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <https://github.com/farhadbaghban/opentelemetry-test.git>
cd <repository-folder>
```
### 2. Install Dependencies
Create a virtual environment and install the required packages:

```bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```
### 3. Run Jaeger in the Background
To enable OpenTelemetry tracing, start a Jaeger instance using Docker:

```bash
docker run -d --name jaeger \
    -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
    -p 5775:5775/udp \
    -p 6831:6831/udp \
    -p 6832:6832/udp \
    -p 5778:5778 \
    -p 16686:16686 \
    -p 14268:14268 \
    -p 14250:14250 \
    -p 9411:9411 \
    jaegertracing/all-in-one:1.41
```
Jaeger will be available at http://localhost:16686.

### 4. Apply Migrations
Before running the projects, migrate the database:

```bash
python manage.py migrate
```

### 5. Run the Development Server
Run the Django development server in a separate terminal:

```bash
python manage.py runserver
```
The User server will be accessible at http://127.0.0.1:8000.
The Order server will be accessible at http://127.0.0.1:8001.
The Trip server will be accessible at http://127.0.0.1:8002.
The Consumer server will be accessible at http://127.0.0.1:8004.

## Usage
        Use test_open for user authentication services.
        Manage orders and items in the test_open_order project.
        Manages Trips and integrates with `test_open` for user information and `test_open_order` for orders.
        Manages the `RequestResponse` and consumes from services for logging data.  
        Trace request flows using OpenTelemetry with Jaeger to monitor interactions.
        OpenTelemetry and Jaeger.

##### This repository includes OpenTelemetry integration for tracing request flows between the two projects. The Jaeger instance collects trace data, providing a visualization of the service interactions.

### Notes
Ensure Docker is installed and running before starting Jaeger.
Migration files are included in the repository. Run python manage.py migrate before using the application.


### 6. Run RabbiyMQ in the Background
To enable services for produce and consume data on RabbitMQ instance using Docker:

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0.5-alpine
```

### License
This repository is for testing purposes and is not intended for production use.
