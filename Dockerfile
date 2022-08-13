FROM python:3.10-slim-buster

# Copy & Change directory
COPY . /nkcrawler/
WORKDIR /nkcrawler

# library update
RUN apt-get update

# pip execution
RUN pip install -U pip
RUN pip install -U setuptools
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "run.py"]