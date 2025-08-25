.PHONY: install test run docker-build docker-run

install:
	pip install -r requirements.txt

test:
	pytest

run:
	python run.py

docker-build:
	docker build -t your-dockerhub-username/expense-tracker:latest .

docker-run:
	docker run --rm -p 5000:5000 \
		-e SECRET_KEY=dev-secret \
		-e DATABASE_URL=sqlite:////data/expense.db \
		-v expense_data:/data \
		--name expense-tracker \
		your-dockerhub-username/expense-tracker:latest
