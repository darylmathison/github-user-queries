FROM python:3

COPY . application/

ENV PYTHONPATH $PYTHONPATH:application

WORKDIR application
RUN pip install -r requirements.txt Twisted

CMD ["twistd", "-n", "web", "--port", "tcp:5000", "--wsgi", "GitHubUserQuery.app"]
