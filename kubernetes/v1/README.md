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

## Полезные команды

1. Удалить кластер

```
$ kind delete cluster --name=filestorage
```

2. Список кластеров

```
$ kind get clusters
```

3. Список докер контейнеров кластера

```
$ docker ps
```

4. Список узлов кластера

```
$ kubectl get nodes -o wide
```

5. Список подов кластера

```
$ kubectl get pods --all-namespaces -o wide
```

6. Список сервисов кластера

```
$ kubectl get services -o wide
```
