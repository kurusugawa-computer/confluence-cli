ifndef SOURCE_FILES
	export SOURCE_FILES:=confluence scripts
endif
ifndef TEST_FILES
	export TEST_FILES:=tests
endif

.PHONY: format lint test docs publish

format:
	poetry run black ${SOURCE_FILES}  ${TEST_FILES} --preview
	poetry run ruff check ${SOURCE_FILES} ${TEST_FILES} --fix-only --exit-zero
	


lint:
	poetry run ruff ${SOURCE_FILES}
	# テストコードはチェックを緩和する
	# pygrep-hooks, flake8-datetimez, line-too-long, flake8-annotations, unused-noqa
	poetry run ruff check ${TEST_FILES} --ignore PGH,DTZ,E501,ANN,RUF100
	poetry run mypy ${SOURCE_FILES}
	poetry run pylint --jobs=0 ${SOURCE_FILES}

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
	
