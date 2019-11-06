build:
	cd ./source \
	&& docker-compose --file ./docker-compose/base.yml build \
	&& docker-compose --file ./docker-compose/excel.yml build \
	&& docker-compose --file ./docker-compose/demo.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml build

up:
	cd ./source && docker-compose --file ./docker-compose/demo.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml up -d

down:
	cd ./source && docker-compose --file ./docker-compose/demo.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml down
