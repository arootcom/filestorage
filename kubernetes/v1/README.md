# Kubernetes

Используем уникальный инструмент [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/), поддерживаемый сообществом [Kubernetes](https://kubernetes.io/). Он создает кластеры Kubernetes внутри контейнеров [Docker](https://www.docker.com/) без любых других зависимостей. Это позволяет моделировать реалистичные кластеры с множеством узлов на локальном компьютере без создания виртуальных машин или использования других тяжеловестных конструкций. Он не подходит для промышленного использования и приминяется только для разработки или иследований.

Далее эксперементы проводил на Ubuntu 22.04.1
Версия Kubernetes:

* Client Version: v1.21.10
* Server Version: v1.21.10

## Запуск кластера

1. Установить Docker

```
$ sudo apt-get install docker
$ docker --version
Docker version 24.0.5, build 24.0.5-0ubuntu1~22.04.1
```

2. Установить kubectl

```
$ curl -LO https://dl.k8s.io/release/v1.21.10/bin/linux/amd64/kubectl
$ curl -LO https://dl.k8s.io/release/v1.21.10//bin/linux/amd64/kubectl.sha256
$ echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
kubectl: OK
```

Если OK, то идем дальше

```
$ chmod +x kubectl
$ mv ./kubectl* ~/.local/bin/
$ kubectl version --client --output=yaml
clientVersion:
  buildDate: "2022-02-16T11:24:04Z"
  compiler: gc
  gitCommit: a7a32748b5c60445c4c7ee904caf01b91f2dbb71
  gitTreeState: clean
  gitVersion: v1.21.10
  goVersion: go1.16.14
  major: "1"
  minor: "21"
  platform: linux/amd64
```

Готово

3. Установить kind

```
$ curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
$ chmod +x ./kind
$ mv ./kind ~/.local/bin/
$ kind --version
kind version 0.23.0
```

4. Создать кластер

```
$ kind create cluster --config=./cluster.yaml
Creating cluster "filestorage" ...
 ✓ Ensuring node image (kindest/node:v1.21.10)
 ✓ Preparing nodes 
 ✓ Writing configuration 
 ✓ Starting control-plane 
 ✓ Installing CNI 
 ✓ Installing StorageClass 
 ✓ Joining worker nodes
Set kubectl context to "kind-filestorage"
You can now use your cluster with:

kubectl cluster-info --context kind-filestorage

Have a nice day!
```

```
$ kubectl version --short
Client Version: v1.21.10
Server Version: v1.21.10
```

## Создание локального репозитория

Воспользуемся официальным образом [Docker Registry](https://registry.hub.docker.com/_/registry/) для хранения и распространения контейнеров и артефактов.

* [About Registry](https://distribution.github.io/distribution/about/)
* [Distribution Registry](https://distribution.github.io/distribution/)
* [Deploy a registry server](https://distribution.github.io/distribution/about/deploying/)

Репозиторий развернем в кластере с хранилищем в инфраструктуре Kubernetes

1. Создать том и выполнить запрос на хранилище

```
$ kubectl apply -f registry-volumes.yaml
``` 

Смотрим, что получилось

```
 $ kubectl get pv,pvc
NAME                               CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                  STORAGECLASS    REASON   AGE
persistentvolume/registry.volume   10Gi       RWO            Retain           Bound    default/registry.pvc   local-storage            3d9h

NAME                                 STATUS   VOLUME            CAPACITY   ACCESS MODES   STORAGECLASS    AGE
persistentvolumeclaim/registry.pvc   Bound    registry.volume   10Gi       RWO            local-storage   3d9h
```

2. Запустить cервис репозитория

```
$ kubectl apply -f registry.yaml 
```

Под запущен и готов к использованию

```
$ kubectl get pods -o wide
NAME                        READY   STATUS    RESTARTS   AGE     IP           NODE                 NOMINATED NODE   READINESS GATES
registry-67cbb5cf9b-nktvn   1/1     Running   0          3d10h   10.244.1.2   filestorage-worker   <none>           <none>
```

3. Проверяем доступность репозитория с наружи кластера

```
 $ curl http://localhost:5000/v2/_catalog
{"repositories":[]}
``` 

4. Проверяем доступность репозитория с ноды кластера

```
$ docker exec -it filestorage-worker curl http://localhost:30000/v2/_catalog
{"repositories":[]}
```

## Загрузка образа в репозиторий

Будем использовать образ сервиса [Humster](../../source/hamster/v1/).

1. Соберем образ сервиса

```
$ cd ../../source/hamster/v1/
$ docker build -t hamster:0.0.1 .
```

Образ собран 

```
$ docker images
REPOSITORY               TAG        IMAGE ID       CREATED        SIZE
hamster                  0.0.1      2848c9a8199e   4 days ago     1.05GB
```

2. Создать тег с указанием репозитория

```
$ docker tag hamster:0.0.1 localhost:5000/hamster:0.0.1
```

```
$ docker images
REPOSITORY               TAG        IMAGE ID       CREATED        SIZE
hamster                  0.0.1      2848c9a8199e   4 days ago     1.05GB
localhost:5000/hamster   0.0.1      2848c9a8199e   4 days ago     1.05GB
```

3. Залить образ в репозиторий

```
$ docker push localhost:5000/hamster:0.0.1
```

4. Проверяем доступность репозитория с ноды кластера

```
$ docker exec -it filestorage-worker curl http://localhost:30000/v2/_catalog
{"repositories":["hamster"]}
```

## Запуск сервиса Humster

1. Создать том и выполнить запрос на хранилище

```
$ kubectl apply -f hamster-volumes.yaml
``` 

Смотрим, что получилось

```
 $ kubectl get pv,pvc
NAME                               CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                  STORAGECLASS    REASON   AGE
persistentvolume/hamster.volume    2Gi        RWO            Retain           Bound    default/hamster.pvc    local-storage            2s
persistentvolume/registry.volume   10Gi       RWO            Retain           Bound    default/registry.pvc   local-storage            25m

NAME                                 STATUS   VOLUME            CAPACITY   ACCESS MODES   STORAGECLASS    AGE
persistentvolumeclaim/hamster.pvc    Bound    hamster.volume    2Gi        RWO            local-storage   2s
persistentvolumeclaim/registry.pvc   Bound    registry.volume   10Gi       RWO            local-storage   25m 
```

2. Запустить cервис репозитория

```
$ kubectl apply -f hamster.yaml 
```

Под запущен и готов к использованию

```
$ kubectl get pods -o wide
NAME                                  READY   STATUS    RESTARTS   AGE   IP           NODE                 NOMINATED NODE   READINESS GATES
hamster-deployment-6c9bffc5fc-2kt92   1/1     Running   0          20m   10.244.1.7   filestorage-worker   <none>           <none>
hamster-deployment-6c9bffc5fc-45bpz   1/1     Running   0          20m   10.244.1.6   filestorage-worker   <none>           <none>
registry-67cbb5cf9b-69dln             1/1     Running   0          24m   10.244.1.5   filestorage-worker   <none>           <none>
```

3. Тестируем систему 

Загружаем тестовый файл

```
$ cd ../../source/hamster/v1/
$ curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@test.txt"  http://localhost:8000/
HTTP/1.1 201 Created
date: Mon, 01 Jul 2024 16:28:22 GMT
server: uvicorn
content-length: 44
content-type: application/json

{"message":"Successfully uploaded test.txt"}
```

Проверяем доступность загруженного файла через API

```
$ curl http://localhost:8000/
{"files":["test.txt"]}
```

Проверяем физическое расположение файла на узле

```
$ docker exec -it filestorage-worker ls /tmp/files
test.txt
```

Проверяем физичекое расположение файлов на нодах, директория которых смотрит на директорию узла. 

```
$ kubectl exec -it hamster-deployment-6c9bffc5fc-2kt92 -- ls /tmp/files
test.txt
$ kubectl exec -it hamster-deployment-6c9bffc5fc-45bpz -- ls /tmp/files
test.txt
```

