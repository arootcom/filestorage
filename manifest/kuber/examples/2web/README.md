# Web

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
$ kubectl get services
NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.96.0.1     <none>        443/TCP    6d4h
my-service   ClusterIP   10.96.5.171   <none>        8080/TCP   8s
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
10.244.0.8      example-pod
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





