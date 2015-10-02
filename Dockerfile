FROM advancedclimatesystems/python:2.7.10

COPY requirements.txt /tmp/requirements.txt
COPY test_requirements.txt /tmp/test_requirements.txt
COPY doc_requirements.txt /tmp/doc_requirements.txt

RUN pip install -r /tmp/doc_requirements.txt
RUN pip install -r /tmp/test_requirements.txt
