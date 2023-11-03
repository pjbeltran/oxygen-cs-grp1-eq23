FROM python:3.8-alpine

WORKDIR /app

COPY Pipfile Pipfile.lock src /app/

RUN pip install pipenv
RUN pipenv install

CMD ["python", "main.py"]
