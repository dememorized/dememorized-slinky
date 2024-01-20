FROM python:3.12


RUN mkdir /python
WORKDIR /python
ADD . /python

ENTRYPOINT pip install poetry && \
    	   poetry install && \
    	   make check