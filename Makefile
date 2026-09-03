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
