build:
	cd ./source \
	&& docker-compose --file ./docker-compose/base.yml build \
	&& docker-compose --file ./docker-compose/excel.yml build \
	&& docker-compose --file ./docker-compose/demo.yml build

up:
	cd ./source && docker-compose --file ./docker-compose/demo.yml up
