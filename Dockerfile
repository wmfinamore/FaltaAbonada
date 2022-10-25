# pull official base image
FROM python:3.10-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 and cryptography dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev cargo jpeg-dev zlib-dev

# create directory for the proto-fiesta user
RUN mkdir -p /home/faltaAbonada

# create the faltaAbonada user
RUN addgroup -S faltaAbonada && adduser -S faltaAbonada -G faltaAbonada

# create the appropriate directories
ENV HOME=/home/faltaAbonada
ENV APP_HOME=/home/faltaAbonada/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
#RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# Install pip
RUN pip install --upgrade pip

# Copy project
COPY . .

#Install dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /home/faltaAbonada/wheels -r requirements.txt

# install dependencies
RUN apk update && apk add libpq
RUN pip install --no-cache /home/faltaAbonada/wheels/*

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

# chown all the files to the app user
RUN chown -R faltaAbonada:faltaAbonada $APP_HOME

# change to the app user
USER faltaAbonada

# run entrypoint.sh
ENTRYPOINT ["/home/faltaAbonada/web/entrypoint.sh"]