setup:
	@echo "not implemented"

up:
	docker-compose up -d app

down:
	docker-compose down --remove-orphans

build:
	docker-compose up --build