# SmartHR
SmartHR - интеллектуальный сервис-помощник служб HR средних и крупных компаний.
Прототип разработан в рамках хакатона Гринатом-2019.

## Сборка и запуск сервиса
### Сборка компонентов сервиса
Сборка компонентов системы осуществляется с помощью команды
```sh
make build
```
В результате успешного выполнения команды будут собраны Docker-образы. Для загрузки Docker-образов в удаленный реестр контейнеров
(в настоящее время в качестве реестра используется сервис Yandex Container Registry) необходимо выполнить команду
```sh
make upload
```
Перед загрузкой образов в удаленный реестр необходимо пройти аутентификацию с помощью команды ```docker login```.

### Генерация данных
Генерация демонстрационных данных осуществляется с помощью команды
```sh
make demo
```

Создание тренировочных и тестовых данных, а также непосредственно тренировки модели
осуществляется с помощью команды
```sh
make train
```
В результате выполнения команды в каталоге data/playbooks/train будут созданы подкаталоги
с искусственно сгенерированными данными. Эта данные используются компонентом *predictor*
для создания модели машинного обучения, предсказывающего вероятность увольнения сотрудника.

### Запуск компонентов сервиса
Для запуска компонентов системы в терминале выполните команду
```sh
make up
```
После запуска Docker-контейнеров в браузере введите адрес http://localhost. В окне браузера будет запущен web-интерфейс системы.

### Останов компонентов сервиса
Для остановки запущенных на компьютере компонентов системы в терминале выполните команду
```sh
make down
```

## Описание компонентов системы
Все компоненты системы разбиты по отдельным Docker-контейнерам. При этом, каждый Docker-контейнер
содержит один и только один компонент сервиса. Контейнеры, равно как и компоненты, подразделяются
на две группы - системные контейнеры и непосредственно контейнеры с логикой сервиса. К системным
компонентам относятся следующие:
 - **kafka** (контейнер *bitnami/kafka*)
 - **zookeeper** (контейнер *bitnami/zookeeper*)
 - **clickhouse** (контейнер *yandex/clickhouse-server*)
 - **deeppavlov_ner_ontonotes** (контейнер *deeppavlov/base-cpu*)
 - **deeppavlov_ner_rus_bert** (контейнер *deeppavlov/base-cpu*)

К компонентам, реализующим непосредственно логику сервиса, относятся:
 - **data** (контейнер *citylix-greenatom-ml/data*)
 - **predictor** (контейнер *citylix-greenatom-ml/predictor*)
 - **engine** (контейнер *citylix-greenatom-ml/engine*)
 - **simulator** (контейнер *citylix-greenatom-ml/simulator*)
 - **fetcher.ping** (контейнер *citylix-greenatom-ml/fetcher.ping*)
 - **fetcher.lync** (контейнер *citylix-greenatom-ml/fetcher.lync*)
 - **fetcher.active_directory** (контейнер *citylix-greenatom-ml/fetcher.active_directory*)
 - **fetcher.exchange** (контейнер *citylix-greenatom-ml/fetcher.exchange*)
 - **fetcher.vk** (контейнер *citylix-greenatom-ml/fetcher.vk*)
 - **fetcher.ok** (контейнер *citylix-greenatom-ml/fetcher.ok*)
 - **fetcher.fb** (контейнер *citylix-greenatom-ml/fetcher.fb*)
 - **fetcher.instagram** (контейнер *citylix-greenatom-ml/fetcher.instagram*)
 - **smtp** (контейнер *citylix-greenatom-ml/smtp*)
 - **www** (контейнер *citylix-greenatom-ml/www*)