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
 ✓ Ensuring node image (kindest/node:v1.21.10) 🖼 
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a nice day! 👋
```

## Материалы

* [Kubernetes](https://kubernetes.io/)
* [Kind](https://kind.sigs.k8s.io/)
* [Install and Set Up kubectl on Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
* [Kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
* [Kind](https://kind.sigs.k8s.io/)
* [kindest/node](https://hub.docker.com/r/kindest/node/tags?page=&page_size=&ordering=&name=1.21.10)
