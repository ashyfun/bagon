FROM python:3.11-alpine3.18

RUN apk add --update --no-cache gcc musl-dev libpq-dev

WORKDIR /var/opt/bagon

COPY requirements.txt ./
RUN pip install -U pip \
    && pip install -r requirements.txt \
    && pip cache purge

COPY ./ ./

EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "-v 3", "0.0.0.0:8000" ]
