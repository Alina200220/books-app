# Используем официальный образ Python в качестве базового образа
#FROM python
# Устанавливаем рабочую директорию внутри контейнера
#WORKDIR /usr/src/app
# Копируем файл requirements.txt внутрь контейнера
#COPY pyproject.toml ./
# Устанавливаем зависимости, описанные в файле requirements.txt
#RUN pip install --user poetry
#ENV PATH="${PATH}:/root/.local/bin"
#RUN poetry install

#FROM python:3
#ENV PYTHONUNBUFFERED 1
#WORKDIR /usr/src/backend
#COPY . .
#COPY poetry.lock pyproject.toml ./
#RUN pip install -U pip && \
#   pip install poetry && \
#   poetry install

FROM python:3.12
WORKDIR /app
COPY requirements.txt ./
# Установите зависимости
#COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .
#COPY app/pyproject.toml app/poetry.lock* /app/
#RUN poetry config virtualenvs.in-project false
#RUN poetry install $(test "$MY_ENV" == env && echo "--no-dev")
#RUN poetry install --no-root
