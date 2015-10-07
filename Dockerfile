FROM advancedclimatesystems/python:2.7.10

COPY requirements.txt /tmp/requirements.txt
COPY dev_requirements.txt /tmp/dev_requirements.txt

RUN pip install -r /tmp/dev_requirements.txt
