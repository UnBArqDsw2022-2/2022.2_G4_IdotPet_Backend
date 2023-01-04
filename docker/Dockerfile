FROM python:3.10 as build-dep
COPY requirements.txt .
RUN mkdir /install
RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install -I --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.10
WORKDIR /app

COPY --from=build-dep /install /usr/local
COPY src /app/src

RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir alembic

CMD ["python3", "src/main.py"]

