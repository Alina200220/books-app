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

FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/backend
COPY . .
COPY poetry.lock pyproject.toml ./
ENV PATH="./.venv/bin:$PATH"
RUN pip install -U pip && \
   pip install poetry && \
   poetry install