FROM ubuntu:16.04

MAINTAINER Your Name "gabriele.nazeri@outlook.it"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# WORKDIR /home/gabriele/PythonCodeExercises/Hangman
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 5000

# ENTRYPOINT [ "bash" ]

# CMD [ "run.sh" ]

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
