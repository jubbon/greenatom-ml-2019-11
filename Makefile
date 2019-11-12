build:
	cd ./source \
	&& docker-compose --file ./docker-compose/base.yml build \
	&& docker-compose --file ./docker-compose/data.yml build \
	&& docker-compose --file ./docker-compose/deeppavlov.yml build \
	&& docker-compose --file ./docker-compose/demo.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml build

train:
	cd ./source \
	&& docker-compose --file ./docker-compose/data.yml build \
	&& docker-compose --file ./docker-compose/data.yml run data python app train 100

demo:
	cd ./source \
	&& docker-compose --file ./docker-compose/data.yml build \
	&& docker-compose --file ./docker-compose/data.yml run data python app demo

up:
	cd ./source \
	&& docker-compose --file ./docker-compose/deeppavlov.yml up -d \
	&& docker-compose --file ./docker-compose/demo.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml up -d

down:
	cd ./source \
	&& docker-compose --file ./docker-compose/deeppavlov.yml down --remove-orphans \
	&& docker-compose --file ./docker-compose/demo.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml down --remove-orphans
