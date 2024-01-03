SERVICE_DIR := tg_bot_template
TXT_BOLD := \e[1m
TXT_MAGENTA := \e[35m
TXT_RESET := \e[0m

setup:
	@poetry install --no-root

setup-pre-commit:
	@poetry run pre-commit install

lint:
	@printf "${TXT_BOLD}${TXT_MAGENTA}========================== BLACK ==============================${TXT_RESET}\n"
	@poetry run black $(SERVICE_DIR)/
	@printf "${TXT_BOLD}${TXT_MAGENTA}======================== END BLACK ============================${TXT_RESET}\n"
	@printf "${TXT_BOLD}${TXT_MAGENTA}=========================== MYPY ==============================${TXT_RESET}\n"
	@poetry run mypy $(SERVICE_DIR)/
	@printf "${TXT_BOLD}${TXT_MAGENTA}========================= END MYPY ============================${TXT_RESET}\n"
	@printf "${TXT_BOLD}${TXT_MAGENTA}=========================== RUFF ==============================${TXT_RESET}\n"
	@poetry run ruff check --fix --show-fixes --exit-non-zero-on-fix .
	@printf "${TXT_BOLD}${TXT_MAGENTA}========================= END RUFF ============================${TXT_RESET}\n"

format:
	@poetry run black $(SERVICE_DIR)/

start_docker:
	docker-compose down && docker-compose up --build -d && docker-compose logs -f

stop_docker:
	docker-compose down

start:
	@poetry run python -m $(SERVICE_DIR).app
