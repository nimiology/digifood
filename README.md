# Online Food Ordering Service API

This project is an Online Food Ordering Service API built with Django REST Framework. It allows users to place orders for various food items from restaurants.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [API Documentation](#api-documentation)

## Installation

To run this API locally, make sure you have the following prerequisites installed:

- Python (>= 3.6)
- Django (>= 3.0)
- Django REST Framework (>= 3.0)

Follow these steps to set up the project:

1. Clone the repository:
```
git clone https://github.com/your-username/food-ordering-api.git
cd food-ordering-api
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
3. Install the required dependencies:

```
pip install -r requirements.txt
```


4. Run database migrations:

```
python manage.py migrate
```
5. Start the development server:

```
python manage.py runserver
```

The API will be accessible at `http://localhost:8000/`.

## Usage

To use the API, you can interact with it through HTTP requests (GET, POST, PUT, DELETE). Here's an overview of the available endpoints:

## Error Handling

The API handles errors gracefully and returns appropriate status codes and error messages. Refer to the documentation for details on error responses.

## Testing

To run the test suite, execute the following command:
```
python manage.py test
```

## Contributing

If you want to contribute to this project, follow the guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

For any questions or suggestions, feel free to contact us at contact@example.com or visit our GitHub repository: [https://github.com/nimiology/digifood](https://github.com/nimiology/digifood)

## API Documentation

The API documentation is available in Swagger UI. You can access it by running the development server and visiting the following URL in your web browser:
```
http://127.0.0.1:8000/swagger
```

Swagger UI provides an interactive interface to explore the API endpoints, their parameters, and responses. It's a helpful tool for understanding how to use the API effectively.
```
http://127.0.0.1:8000/redoc
```

Additionally, if you prefer the ReDoc documentation style, you can access it at the above URL.

