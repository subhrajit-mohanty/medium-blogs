gunicorn -k uvicorn.workers.UvicornWorker --workers 1 --threads=1 --max-requests 512 --bind 0.0.0.0:8050 app:app