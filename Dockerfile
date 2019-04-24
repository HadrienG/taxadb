FROM python:3

MAINTAINER Hadrien Gourlé <gourlehadrien@gmail.com>

WORKDIR /usr/src/app

RUN pip install taxadb

CMD [ "taxadb" ]
