export DOCKER_IMAGE_REGISTRY=cr.yandex/crphj01dfoo9goar48sq
export DOCKER_IMAGE_TAG=latest

build:
	cd ./source \
	&& docker-compose --file ./docker-compose/base.yml build \
	&& docker-compose --file ./docker-compose/data.yml build \
	&& docker-compose --file ./docker-compose/deeppavlov.yml build \
	&& docker-compose --file ./docker-compose/app.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml build

upload:
	cd ./source \
	&& docker-compose --file ./docker-compose/base.yml push \
	&& docker-compose --file ./docker-compose/data.yml push \
	&& docker-compose --file ./docker-compose/app.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml push --ignore-push-failures

dataset:
	cd ./source \
	&& docker-compose --file ./docker-compose/data.yml build \
	&& docker-compose --file ./docker-compose/data.yml run data python app --activity train 100

train:
	cd ./source \
	&& docker-compose --file ./docker-compose/app.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml run predictor python app/train.py \

demo:
	cd ./source \
	&& docker-compose --file ./docker-compose/data.yml build \
	&& docker-compose --file ./docker-compose/data.yml run data python app demo

predict:
	cd ./source \
	&& docker-compose --file ./docker-compose/app.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml run --build predictor python app/predict.py

up:
	cd ./source \
	&& docker-compose --file ./docker-compose/deeppavlov.yml up -d \
	&& docker-compose --file ./docker-compose/app.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml up -d

down:
	cd ./source \
	&& docker-compose --file ./docker-compose/deeppavlov.yml down --remove-orphans \
	&& docker-compose --file ./docker-compose/app.yml --file ./docker-compose/kafka.yml --file ./docker-compose/clickhouse.yml down --remove-orphans
