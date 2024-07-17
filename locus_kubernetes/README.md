## FastAPI Application

This repository includes a sample FastAPI application in the `app/` directory. This application serves as the target for our Locust load tests.

To run the FastAPI application locally:

1. Navigate to the `app/` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `uvicorn main:app --reload`

For deploying to Kubernetes, you'll need to build a Docker image and update the `kubernetes/fastapi-deployment.yaml` file with the correct image name.

## Documentation

- [Setup Guide](docs/SETUP.md)
- [Usage Guide](docs/USAGE.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.