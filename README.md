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
 - **kafka** (контейнер *bitnami/kafka*) - распределенная очередь сообщений, которая связывает между
 собой другие компоненты сервиса.
 - **zookeeper** (контейнер *bitnami/zookeeper*) - сервис координации, используемый сервисом **kafka**.
 - **clickhouse** (контейнер *yandex/clickhouse-server*) - аналитическая (колоночная) база данных, используемая
 для хранения информации о событиях с сотрудниками
 - **deeppavlov_ner_ontonotes** (контейнер *deeppavlov/base-cpu*) - API-сервис для распознавания тональности текста
 (отрицательная тональность, нейтральная тональность, положительная тональность)
 - **deeppavlov_ner_rus_bert** (контейнер *deeppavlov/base-cpu*) - API-сервис для распознавания именованных сущностей
 (ФИО, названия проектов и организаций, локаций и т.д.)

К компонентам, реализующим непосредственно логику сервиса, относятся:
 - **data** (контейнер *citylix-greenatom-ml/data*) - отвечает за генерацию фейковых данных для демонстрации работы сервиса,
 а также данных, используемых для тренировки и валидации модели машинного обучения (вероятность увольнения сотрудника).
 - **predictor** (контейнер *citylix-greenatom-ml/predictor*) - осуществляет тренировку модели машинного обучения (вероятность
 увольнения сотрудника) и
 - **engine** (контейнер *citylix-greenatom-ml/engine*)
 - **simulator** (контейнер *citylix-greenatom-ml/simulator*) - симулятор поведения сотрудников, который является ключевым компонентом
 "цифрового двойника"
 - **fetcher.ping** (контейнер *citylix-greenatom-ml/fetcher.ping*)
 - **fetcher.lync** (контейнер *citylix-greenatom-ml/fetcher.lync*) - отвечает за сборку данных о переписке сотрудников между собой
 через службу *Skype for Business* (ранее *Microsoft Lync*)
 - **fetcher.active_directory** (контейнер *citylix-greenatom-ml/fetcher.active_directory*) - отвечает за сборку данных из службы
 *Active Directory*
 - **fetcher.exchange** (контейнер *citylix-greenatom-ml/fetcher.exchange*) - отвечает за сборку данных из службы
 *Microsoft Exchange*
 - **fetcher.vk** (контейнер *citylix-greenatom-ml/fetcher.vk*) - выполняет сбор и структуризацию открытых данных о сотрудниках
 из социальной сети ВКонтакте
 - **fetcher.ok** (контейнер *citylix-greenatom-ml/fetcher.ok*) - выполняет сбор и структуризацию открытых данных о сотрудниках
 из социальной сети Одноклассники
 - **fetcher.fb** (контейнер *citylix-greenatom-ml/fetcher.fb*)  - выполняет сбор и структуризацию открытых данных о сотрудниках
 из социальной сети Facebook
 - **fetcher.instagram** (контейнер *citylix-greenatom-ml/fetcher.instagram*) - выполняет сбор и структуризацию открытых данных о сотрудниках
 из социальной сети Instagram
 - **smtp** (контейнер *citylix-greenatom-ml/smtp*) - отправляет сообщения по электронной почте
 - **www** (контейнер *citylix-greenatom-ml/www*) - web-приложение, обеспечивающее интерактивное взаимодействие сервиса с пользователем