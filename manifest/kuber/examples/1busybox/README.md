# BusyBox

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

Посмотреть все кластеры

```
$ kind get clusters
kind
```

Так можно посмотреть, какие модули Pod выполняются в кластере.

```
$ kubectl get pods -o wide --all-namespaces
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

## Запуск Pod 

Обычно модули Pod создаются не в ручную, а спомощью объектов Deployment, DaemonSet или Job.
Но пока создадим простой одиночный модуль Pod, используя для этого

```
$ kubectl create -f pod.yaml 
pod/core-k8s created
```

Список Pods

```
$ kubectl get pods
NAME       READY   STATUS    RESTARTS   AGE
core-k8s   1/1     Running   0          7m59s
```

Объект Pod на сервере хранит полную информацию о состоянии модуля

```
$ kubectl get pods -o yaml
```

## Исследование Pod

Запросить состояние модуля Pod

```
$ kubectl get pods -o=jsonpath='{.items[0].status.phase}'
Running
```

Запросить IP 

```
$ kubectl get pods -o=jsonpath='{.items[0].status.podIP}'
10.244.0.5
```

Запросить IP хоста на котром выполняется модуль

```
$ kubectl get pods -o=jsonpath='{.items[0].status.hostIP}'
172.21.0.2
```

Информация о DNS

```
$ kubectl exec -i -t core-k8s -- mount | grep resolv
/dev/nvme0n1p2 on /etc/resolv.conf type ext4 (rw,relatime,errors=remount-ro)
```

## Удаление Pod

```
$ kubectl delete -f ./pod.yaml 
pod "core-k8s" deleted
```
