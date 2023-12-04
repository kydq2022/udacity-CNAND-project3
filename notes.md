```shell
kubectl --namespace monitoring port-forward svc/prometheus-grafana --address 0.0.0.0 3000:80
```

```shell
kubectl port-forward svc/frontend-service  --address 0.0.0.0  8080:8080
```