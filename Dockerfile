FROM python:3.8-alpine

WORKDIR /app

COPY Pipfile Pipfile.lock src /app/

ENV HOST "https://hvac-simulator-a23-y2kpq.ondigitalocean.app"
ENV TOKEN "WeVCNw8DOZ"
ENV TICKETS 2
ENV T_MAX 30
ENV T_MIN 18
ENV DATABASE "log680"

RUN pip install pipenv
RUN pipenv install

CMD ["pipenv", "run", "python", "/app/main.py"]