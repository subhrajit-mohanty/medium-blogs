## Running a Load Test

1. Get the cluster IP of the FastAPI service:

`kubectl get service fastapi-app`

2. In the Locust web interface, enter the number of users to simulate
3. Set the spawn rate (users spawned/second)
4. Enter the host to test against: `http://<CLUSTER-IP>`
5. Click "Start swarming"

## Monitoring

- View Locust statistics in the web interface
- Monitor pod status: `kubectl get pods`
- Check HPA status: `kubectl get hpa`
- View logs: `kubectl logs <pod-name>`

## Stopping the Test

1. Click "Stop" in the Locust web interface
2. (Optional) Scale down the worker deployment:

`kubectl scale deployment locust-worker --replicas=0`

## Cleanup

To remove all Locust resources from your cluster:

`kubectl delete -f kubernetes/`

