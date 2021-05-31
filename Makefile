setup:
	mkdir -p data/member_stats data/team_info data/seasonal_stats && \
cp -n sample.env .env && \
mkdir -p logs/cron

up:
	docker-compose up -d redis database

down:
	docker-compose down --remove-orphans

build:
	docker-compose up --build --no-start --no-deps