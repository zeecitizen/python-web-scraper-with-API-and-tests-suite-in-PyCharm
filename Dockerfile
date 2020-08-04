FROM python:3.6-slim

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip

RUN pip install BeautifulSoup4
RUN pip install lxml
RUN pip install pyyaml

ENV PYTHONPATH ":/app"

RUN pip install -r requirements.txt

CMD python main.py --html_path="/app/html/example.html"
