FROM python:3.9
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-pip

RUN mkdir /code
WORKDIR /code

# Add path to django-admin.py
ENV PATH="/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /code/
RUN python3 -m venv /venv
RUN /venv/bin/pip install --upgrade setuptools && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install Django==3.2.9 && \
    /venv/bin/pip install -r requirements.txt