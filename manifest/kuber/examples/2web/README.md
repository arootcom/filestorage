# Web


## Создать кластер

Удалить прежний кластер, если имеется

```
$ kind delete cluster --name=kind
Deleting cluster "kind" ...
```

Создать новый кластер

```
$ kind create cluster --config=./cluster.yaml 
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.21.10)
 ✓ Preparing nodes 
 ✓ Writing configuration
 ✓ Starting control-plane
 ✓ Installing StorageClass
 ✓ Joining worker nodes 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a nice day!
```

```
$ kind get clusters
kind
```

```
$ kubectl get rc,nodes
NAME                      STATUS   ROLES                  AGE   VERSION
node/kind-control-plane   Ready    control-plane,master   40m   v1.21.10
node/kind-worker          Ready    <none>                 39m   v1.21.10
```

```
$ docker ps
CONTAINER ID   IMAGE                   COMMAND                  CREATED         STATUS         PORTS                                      NAMES
4133c285d22d   kindest/node:v1.21.10   "/usr/local/bin/entr…"   2 minutes ago   Up 2 minutes   0.0.0.0:80->80/tcp, 0.0.0.0:433->433/tcp   kind-worker
b61d09b612e2   kindest/node:v1.21.10   "/usr/local/bin/entr…"   2 minutes ago   Up 2 minutes   127.0.0.1:39263->6443/tcp                  kind-control-plane
```

## Web Pod

Запуск простого веб приложения на pyton

```
$ kubectl create -f ./pod-web.yaml 
pod/example-pod created
```

Проверяем статус

```
$ kubectl get pods
NAME          READY   STATUS    RESTARTS   AGE
example-pod   1/1     Running   0          28s
```

Проверяем доступность внутри контейнера

```
$ kubectl exec -i -t example-pod -- curl -v http://localhost:8080/etc/hosts
*   Trying 127.0.0.1:8080...
* Connected to localhost (127.0.0.1) port 8080 (#0)
> GET /etc/hosts HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.88.1
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: SimpleHTTP/0.6 Python/3.12.4
< Date: Sun, 16 Jun 2024 13:01:07 GMT
< Content-type: application/octet-stream
< Content-Length: 206
< Last-Modified: Sun, 16 Jun 2024 12:53:06 GMT
< 
# Kubernetes-managed hosts file.
127.0.0.1       localhost
10.244.0.8      example-pod
* Closing connection 0
```

## Web Service

Экспортируем containerPort через стандартный сервис ClusterIP. Это самый простой из всех сервисов Kebernetes, он сообщает  kube-proxy о необходимости создать один виртуальный IP адрес связанный с example-pod

```
$ kubectl create -f ./service-web.yaml 
service/my-service created
```

```
$ kubectl get rc,services
NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    37m
service/my-service   ClusterIP   10.96.194.221   <none>        8080/TCP   17m
```

## Доступ в кластере

Создадим простой образ Docker, для работы с сервисами в нашем кластере.

```
$ kubectl create -f ./sleep.yaml 
pod/sleep created
```

```
$ kubectl get pods
NAME          READY   STATUS    RESTARTS   AGE
example-pod   1/1     Running   0          26m
sleep         1/1     Running   0          67s
```

```
$ kubectl exec -it sleep -- curl -v http://my-service:8080//etc/hosts
*   Trying 10.96.5.171...
* TCP_NODELAY set
* Connected to my-service (10.96.5.171) port 8080 (#0)
> GET //etc/hosts HTTP/1.1
> Host: my-service:8080
> User-Agent: curl/7.58.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: SimpleHTTP/0.6 Python/3.12.4
< Date: Sun, 16 Jun 2024 13:22:24 GMT
< Content-type: application/octet-stream
< Content-Length: 206
< Last-Modified: Sun, 16 Jun 2024 12:53:06 GMT
< 
# Kubernetes-managed hosts file.
127.0.0.1       localhost
192.168.0.5     example-pod
* Closing connection 0
```

Результат:

* Модуль example-pod работает и позволяет посмотреть содержимое файлов ОС через порт 8080
* Любой модуль Pod в кластере может обратиться к этому сервису через порт 8080 благодаря созданому сервису my-service
* kebe-proxy пересылает трафик из my-service в example-pod и создает соответсвующие правила в iptables
* Провайдер CNI способен создавать необходимые правила маршрутизации и пересылать трафик между IP адресами модулей после переадресациями правидами iptables


## Доступ из вне

Есть енсколько видов контроллеров. Наибольшей популярностью ползуются Nginx и Countour.

## Countour

```
$ git clone https://github.com/projectcontour/contour.git
$ kubectl apply -f ./contour/examples/contour/ --validate=false
```

```
$ sudo 'echo "127.0.0.1 my-service.local" >> /etc/hosts'
$ ping my-service.local
PING my-service.local (127.0.0.1) 56(84) bytes of data.
64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.053 ms
64 bytes from localhost (127.0.0.1): icmp_seq=2 ttl=64 time=0.087 ms
```

```
$ kubectl create -f ./contour.yaml 
ingress.networking.k8s.io/example-ingress created
```

```
$ kubectl get rc,services --all-namespaces
NAMESPACE        NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
default          service/kubernetes   ClusterIP      10.96.0.1       <none>        443/TCP                      35m
default          service/my-service   ClusterIP      10.96.194.221   <none>        8080/TCP                     15m
kube-system      service/kube-dns     ClusterIP      10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP       35m
projectcontour   service/contour      ClusterIP      10.96.104.112   <none>        8001/TCP                     3m34s
projectcontour   service/envoy        LoadBalancer   10.96.169.126   <pending>     80:30886/TCP,443:31398/TCP   3m34s
```


```
$ curl -v  http://my-service.local/etc/hosts
*   Trying 127.0.0.1:80...
* Connected to my-service.local (127.0.0.1) port 80 (#0)
> GET /etc/hosts HTTP/1.1
> Host: my-service.local
> User-Agent: curl/7.81.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< server: envoy
< date: Mon, 17 Jun 2024 07:36:35 GMT
< content-type: application/octet-stream
< content-length: 207
< last-modified: Sun, 16 Jun 2024 18:17:17 GMT
< x-envoy-upstream-service-time: 1
< 
# Kubernetes-managed hosts file.
127.0.0.1       localhost
192.168.0.5     example-pod
* Connection #0 to host my-service.local left intact
```



