build:
	cd ./source && docker-compose --file ./docker-compose/demo.yml build

up:
	cd ./source && docker-compose --file ./docker-compose/demo.yml up
