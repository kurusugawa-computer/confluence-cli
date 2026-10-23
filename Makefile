GITLEAKS_VERSION := v8.30.1
GITLEAKS_DOCKER_CONFIG ?=

ifndef SOURCE_FILES
	export SOURCE_FILES:=confluence
endif
ifndef TEST_FILES
	export TEST_FILES:=tests
endif

.PHONY: format lint test docs publish

format:
	uv run ruff format ${SOURCE_FILES}  ${TEST_FILES}
	uv run ruff check ${SOURCE_FILES} ${TEST_FILES} --fix-only --exit-zero



lint:
	uv run ruff check ${SOURCE_FILES} ${TEST_FILES}
	uv run mypy ${SOURCE_FILES}

test:
	# 並列実行してレポートも出力する
	uv run pytest -n auto --cov=confluence --cov-report=html tests

docs:
	cd docs && uv run make html

.PHONY: gitleaks

gitleaks:
	@if command -v gitleaks >/dev/null 2>&1; then \
		gitleaks git --redact=100 --verbose --log-opts=HEAD .; \
	elif command -v docker >/dev/null 2>&1; then \
		if [ -n "${GITLEAKS_DOCKER_CONFIG}" ]; then \
			mkdir -p "${GITLEAKS_DOCKER_CONFIG}"; \
			export DOCKER_CONFIG="${GITLEAKS_DOCKER_CONFIG}"; \
		fi; \
		docker run --rm \
			-v "$$(pwd):$$(pwd):ro" \
			-v "$$(git rev-parse --path-format=absolute --git-common-dir):$$(git rev-parse --path-format=absolute --git-common-dir):ro" \
			-w "$$(pwd)" ghcr.io/gitleaks/gitleaks:${GITLEAKS_VERSION} git --redact=100 --verbose --log-opts=HEAD .; \
	else \
		echo "gitleaksまたはdockerをインストールしてください。" >&2; \
		exit 127; \
	fi
