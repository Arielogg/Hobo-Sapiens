FROM python:3

WORKDIR /usr/src/app

COPY src/main/resources/requirements.txt ./
RUN pip install -r requirements.txt
RUN pip uninstall -y urllib3
RUN pip install urllib3
COPY src/main/python .

CMD ["python", "./runner.py", "filter.json"]