COMPOSE := docker compose

.PHONY: dev down build version

dev:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

build:
	$(COMPOSE) run --build --rm hugo --minify --environment production --destination /cache/public --noBuildLock --panicOnWarning

version:
	$(COMPOSE) run --build --rm hugo version
