# Описание

## Глосарий

**OCI** (Open Container Initiative ) - это группа компаний, которые поддерживают спецификацию формата образа контейнера и метода запуска контейнеров


**Pod** - это модуль, содержащий один или несколько образов OCI, которые выполняются в контейнерах на односм узле кластера Kubernetes.

**Node** (Узел Kubernetes) - это отдельная еденица вычислительной инфраструктуры (сервер), на которой выполняется kubelet

**kubelet** - это двичная программа, играющая роль агента и взаимодействующая с сервером Kubernetes API посредством поддержки цикла управления. Она работает на каждом узле, без этой программы узел Kubernetes недоступен планировщику и не может считаться частью кластера.



**CRI** (Container Runtime Interface) - Интейрфейс реды выполнения отвечающий за запуск контейнеров

**CNI** (Container Network Interface) - Сетевой интерфейс отвечающий за предоставление контейнерам IP-адресов

**CSI** (Container Storage Interface) - Интерфейс контейнерного хранилища. Создан, что бы поставщики решений для организации хранилищ могли легко подключаться к любому кластеру Kubernetes и предоставлять широкий спектр возможностей хранения данных.



**CRD** (Custom Resource Definition) - Определения пользовательских ресурсов

**SDN** (Software-Defined Networking) Позволяет перенастраивать сети больших центров обработки данныхt 

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

## Полезные ссылки

* [Kubernetes](https://kubernetes.io/)
* [Install and Set Up kubectl on Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
* [Command line tool (kubectl)](https://kubernetes.io/docs/reference/kubectl/)
* [Kind](https://kind.sigs.k8s.io/)
* [Kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
* [Kind configuration](https://kind.sigs.k8s.io/docs/user/configuration/)
* [kindest/node](https://hub.docker.com/r/kindest/node/tags?page=&page_size=&ordering=&name=1.21.10)
