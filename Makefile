init: .venv
	pip install --upgrade pip
	pip install -r requirements.txt
	cd awstools && make init

.venv:
	python3 -m venv .venv
