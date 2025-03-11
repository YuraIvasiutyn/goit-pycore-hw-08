FROM python:3.12

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv

RUN pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 5000

ENTRYPOINT ["pipenv", "run", "python", "main.py"]