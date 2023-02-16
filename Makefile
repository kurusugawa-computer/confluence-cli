ifndef FORMAT_FILES
	export FORMAT_FILES:=kci tests
endif
ifndef LINT_FILES
	export LINT_FILES:=kci
endif

.PHONY: format lint test docs publish

format:
	poetry run autoflake  --in-place --remove-all-unused-imports  --ignore-init-module-imports --recursive ${FORMAT_FILES}
	poetry run isort ${FORMAT_FILES}
	poetry run black ${FORMAT_FILES}

lint:
	poetry run mypy ${LINT_FILES}
	poetry run flake8 ${LINT_FILES}
	poetry run pylint --jobs=0 ${LINT_FILES}

test:
	# 並列実行してレポートも出力する
	poetry run pytest -n auto  --cov=kci --cov-report=html tests

docs:
	cd docs && poetry run make html

# publish:
# 	# public PyPIにデプロイ 
# 	poetry publish --build
# 	# 社内PyPIにデプロイ
# 	# 事前に`$ poetry config repositories.kci-upload https://kurusugawa.jp/nexus3/repository/KRS-pypi/ `を実行すること
# 	poetry publish --repository kci-upload --build
	
