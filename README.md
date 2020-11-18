# Test RST in AKS with Python client

```shell script
kubectl apply -f rbac.yaml
kubectl apply -f deploy.yaml
```

The tcpdump sidecar will collect the logs of the pod and save it to /shared-data.