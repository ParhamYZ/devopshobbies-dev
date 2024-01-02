# This docker file is used for production
# Creating image based on official python3 image
FROM python:3.10
ENV HOME=/app
ENV APP_HOME=/app/backend
# keeps python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app && \
    groupadd -r appuser && useradd --no-log-init -r -g appuser appuser && \
    python -m pip install --upgrade pip && \
    mkdir ${APP_HOME} ${APP_HOME}/logs

WORKDIR ${APP_HOME}
EXPOSE 8000


# Install pip requirements
COPY requirements.txt ${APP_HOME}
RUN python -m pip install -r requirements.txt

# Copy all files
COPY . ${APP_HOME}

RUN pip install ipython==8.2.0 && pip install gunicorn==20.1.0
