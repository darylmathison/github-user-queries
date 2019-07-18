FROM python:3

COPY . application/

ENV PYTHONPATH $PYTHONPATH:application
ENV PORT 8080

WORKDIR application
RUN pip install -r requirements.txt Twisted

CMD twistd -n web --port tcp:$PORT --wsgi GitHubUserQuery.app
