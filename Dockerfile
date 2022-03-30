FROM python:3.9

ENV FLASK_APP=cloud_browser
ENV VIRTUAL_ENV=/opt/venv

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN flask init-database

EXPOSE 5000

COPY main.py .
CMD ["python", "./main.py"]
