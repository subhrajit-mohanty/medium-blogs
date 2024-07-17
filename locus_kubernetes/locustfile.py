from locust import HttpUser, task, between
import json

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_root(self):
        self.client.get("/")

    @task(2)
    def get_items(self):
        self.client.get("/items")

    @task(1)
    def create_item(self):
        item = {"name": "Test Item", "price": 10.99}
        self.client.post("/items", json=item)

    @task(2)
    def get_item(self):
        self.client.get("/items/1")

    @task(1)
    def slow_request(self):
        self.client.get("/slow")