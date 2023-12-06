```shell
kubectl --namespace monitoring port-forward svc/prometheus-grafana --address 0.0.0.0 3000:80
```

```shell
kubectl port-forward svc/frontend-service  --address 0.0.0.0  8080:8080
```

```
sudo docker build -t kydq2022/project3-backend:v4 .

sudo docker push kydq2022/project3-backend:v4
```

```
sudo docker build -t kydq2022/project3-frontend:v4 .

sudo docker push kydq2022/project3-frontend:v4
```


```
kubectl apply -f backend.yaml
kubectl get deployment,svc,pods
```

```
kubectl apply -f frontend.yaml
kubectl get deployment,svc,pods
```

```
kydq2022/project3-frontend:v4

sudo docker save kydq2022/project3-frontend:v4 | sudo k3s ctr images import -

sudo docker save kydq2022/project3-backend:v4 | sudo k3s ctr images import -
```