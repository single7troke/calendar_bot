.DEFAULT_GOAL := help
THIS_FILE := $(lastword $(MAKEFILE_LIST))
help:
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

run:
	docker-compose -f config/dev/polling.yml up -d

stop:
	docker-compose -f config/dev/polling.yml down --remove-orphans

run_webhook:
	docker-compose -f config/dev/webhook.yml up -d

stop_webhook:
	docker-compose -f config/dev/polling.yml down -v --remove-orphans

build:
	docker image rm dev-bot dev-app dev-watcher
	docker-compose -f config/dev/polling.yml build

restart_bot:
	docker stop dev-bot-1
	docker start dev-bot-1
