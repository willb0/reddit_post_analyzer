FROM --platform=$BUILDPLATFORM python:3.10-slim

WORKDIR /usr/src/api

RUN apt-get update

COPY requirements.txt /usr/src/api/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY ./ /usr/src/api/

RUN python -c "import nltk;nltk.download('stopwords');nltk.download('words');"

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","80"]


