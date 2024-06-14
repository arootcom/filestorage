# Kubernetes

Используем уникальный инструмент Kind, поддерживаемый сообществом Kubernetes. Он создает кластеры Kubernetes внутри контейнеров Docker без любых других зависимостей. Это позволяет моделировать реалистичные кластеры с множеством узлов на локальном компьютере без создания виртуальных машин или использования других тяжеловестных конструкций. Он не подходит для промышленного использования и приминяется только для разработки или иследований.

## Установить Docker

```
$ docker --version
Docker version 24.0.5, build 24.0.5-0ubuntu1~22.04.1
```

## Установить kubectl

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

## Установить kind

```
$ curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
$ chmod +x ./kind
$ mv ./kind ~/.local/bin/
$ kind --version
kind version 0.23.0
```

## Создать кластер

Удалить прежний кластер, если имеется

```
$ kind delete cluster --name=kind
Deleting cluster "kind" ...
```

Создать новый кластер

```
$ kind create cluster --image kindest/node:v1.21.10
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.21.10)
 ✓ Preparing nodes
 ✓ Writing configuration
 ✓ Starting control-plane
 ✓ Installing CNI
 ✓ Installing StorageClass
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a nice day!
```

Так можно посмотреть, какие модули Pod выполняются в кластере.

```
$ kubectl get pods --all-namespaces
NAMESPACE            NAME                                         READY   STATUS    RESTARTS   AGE
kube-system          coredns-558bd4d5db-bsngw                     1/1     Running   0          71m
kube-system          coredns-558bd4d5db-c8zn6                     1/1     Running   0          71m
kube-system          etcd-kind-control-plane                      1/1     Running   0          71m
kube-system          kindnet-b5mb6                                1/1     Running   0          71m
kube-system          kube-apiserver-kind-control-plane            1/1     Running   0          71m
kube-system          kube-controller-manager-kind-control-plane   1/1     Running   0          71m
kube-system          kube-proxy-dv8dp                             1/1     Running   0          71m
kube-system          kube-scheduler-kind-control-plane            1/1     Running   0          71m
local-path-storage   local-path-provisioner-74567d47b4-ntpqn      1/1     Running   0          71m
```

Что бы посмотреть, где находиться узел Kubernetes, достаточно спросить об этом Docker

```
$ docker ps
CONTAINER ID   IMAGE                   COMMAND                  CREATED             STATUS             PORTS                       NAMES
16f1e7d4cdcf   kindest/node:v1.21.10   "/usr/local/bin/entr…"   About an hour ago   Up About an hour   127.0.0.1:44525->6443/tcp   kind-control-plane
```

Что бы подключиться к узлу, нужно выполнить следующую команду

```
$ docker exec -i -t 16f1e7d4cdcf /bin/bash
root@kind-control-plane:/# kubelet --version
Kubernetes v1.21.10
```

## Глосарий

CRI - Container Runtime Interface. Интейрфейс реды выполнения отвечающий за запуск контейнеров
CNI - Container Network Interface. Сетевой интерфейс отвечающий за предоставление контейнерам IP-адресов
SDN - Software-Defined Networking. Позволяет перенастраивать сети больших центров обработки данных

## Материалы

* [Kubernetes](https://kubernetes.io/)
* [Kind](https://kind.sigs.k8s.io/)
* [Install and Set Up kubectl on Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
* [Kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
* [Kind](https://kind.sigs.k8s.io/)
* [kindest/node](https://hub.docker.com/r/kindest/node/tags?page=&page_size=&ordering=&name=1.21.10)
