build:
	make cmd TARGET:="docker compose build"

up:
	make cmd TARGET:="docker compose up -d"

down:
	make cmd TARGET:="docker compose down"

restart:
	make cmd TARGET:="docker compose restart"

ps:
	make cmd TARGET:="docker compose ps"

setup:
	@make build
	@make up

exec-app:
	make cmd TARGET:="docker compose exec app bash"

start:
	make cmd TARGET:="docker compose exec app bash -c 'python main.py'"

fresh:
	rm -rf ./src/data/evaluation/*; \
	rm -rf ./src/data/result/*

cmd:
ifeq ($(OS),Windows_NT)
	winpty $(TARGET)
else
	$(TARGET)
endif