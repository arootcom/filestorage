# Kubernetes

Используем уникальный инструмент Kind, поддерживаемый сообществом Kubernetes. Он создает кластеры Kubernetes внутри контейнеров Docker без любых других зависимостей. Это позволяет моделировать реалистичные кластеры с множеством узлов на локальном компьютере без создания виртуальных машин или использования других тяжеловестных конструкций. Он не подходит для промышленного использования и приминяется только для разработки или иследований.

* [Материалы про Kubernetes](./info/)

Далее эксперементы проводил на Ubuntu 22.04.1
Версия Kubernetes:

    * Client Version: v1.21.10
    * Server Version: v1.21.10

## Установить Docker

```
$ sudo apt-get install docker
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

## Удалить кластер

```
$ kind delete cluster --name=filestorage
Deleting cluster "filestorage" ...
Deleted nodes: ["filestorage-control-plane" "filestorage-worker"]
```

## Создать кластер

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

## Список кластеров

```
$ kind get clusters
filestorage
```

## Список докер контейнеров кластера

```
$ docker ps
CONTAINER ID   IMAGE                   COMMAND                  CREATED              STATUS              PORTS                                      NAMES
9e11f66a6d37   kindest/node:v1.21.10   "/usr/local/bin/entr…"   About a minute ago   Up About a minute   127.0.0.1:34199->6443/tcp                  filestorage-control-plane
0ebb8d109184   kindest/node:v1.21.10   "/usr/local/bin/entr…"   About a minute ago   Up About a minute   0.0.0.0:80->80/tcp, 0.0.0.0:433->433/tcp   filestorage-worker2
2a18278fcb84   kindest/node:v1.21.10   "/usr/local/bin/entr…"   About a minute ago   Up About a minute                                              filestorage-worker
```

## Список узлов кластера

```
$ kubectl get nodes -o wide
NAME                        STATUS   ROLES                  AGE    VERSION    INTERNAL-IP   EXTERNAL-IP   OS-IMAGE       KERNEL-VERSION     CONTAINER-RUNTIME
filestorage-control-plane   Ready    control-plane,master   2m9s   v1.21.10   172.21.0.4    <none>        Ubuntu 21.10   6.5.0-35-generic   containerd://1.5.10
filestorage-worker          Ready    <none>                 97s    v1.21.10   172.21.0.2    <none>        Ubuntu 21.10   6.5.0-35-generic   containerd://1.5.10
filestorage-worker2         Ready    <none>                 97s    v1.21.10   172.21.0.3    <none>        Ubuntu 21.10   6.5.0-35-generic   containerd://1.5.10
```

### Список подов кластера

```
$ kubectl get pods --all-namespaces -o wide
NAMESPACE            NAME                                                READY   STATUS    RESTARTS   AGE     IP           NODE                        NOMINATED NODE   READINESS GATES
kube-system          coredns-558bd4d5db-7qfht                            1/1     Running   0          2m35s   10.244.0.4   filestorage-control-plane   <none>           <none>
kube-system          coredns-558bd4d5db-xjh5f                            1/1     Running   0          2m35s   10.244.0.2   filestorage-control-plane   <none>           <none>
kube-system          etcd-filestorage-control-plane                      1/1     Running   0          2m48s   172.21.0.4   filestorage-control-plane   <none>           <none>
kube-system          kindnet-84slb                                       1/1     Running   0          2m20s   172.21.0.2   filestorage-worker          <none>           <none>
kube-system          kindnet-8ljqg                                       1/1     Running   0          2m35s   172.21.0.4   filestorage-control-plane   <none>           <none>
kube-system          kindnet-kch8x                                       1/1     Running   0          2m20s   172.21.0.3   filestorage-worker2         <none>           <none>
kube-system          kube-apiserver-filestorage-control-plane            1/1     Running   0          2m49s   172.21.0.4   filestorage-control-plane   <none>           <none>
kube-system          kube-controller-manager-filestorage-control-plane   1/1     Running   0          2m49s   172.21.0.4   filestorage-control-plane   <none>           <none>
kube-system          kube-proxy-6556p                                    1/1     Running   0          2m35s   172.21.0.4   filestorage-control-plane   <none>           <none>
kube-system          kube-proxy-qxsv2                                    1/1     Running   0          2m20s   172.21.0.2   filestorage-worker          <none>           <none>
kube-system          kube-proxy-txjrl                                    1/1     Running   0          2m20s   172.21.0.3   filestorage-worker2         <none>           <none>
kube-system          kube-scheduler-filestorage-control-plane            1/1     Running   0          2m49s   172.21.0.4   filestorage-control-plane   <none>           <none>
local-path-storage   local-path-provisioner-74567d47b4-d8cgt             1/1     Running   0          2m35s   10.244.0.3   filestorage-control-plane   <none>           <none>
```

## Список сервисов кластера

```
$ kubectl get services -o wide
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE     SELECTOR
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   3m58s   <none>
```
