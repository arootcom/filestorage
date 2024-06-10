# BusyBox

# Запуск Pod 

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

# Исследование Pod

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

