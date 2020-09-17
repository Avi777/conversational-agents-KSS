FROM python:3.8-slim-buster

MAINTAINER Avi777 avishekh@fusemachines.com

RUN apt-get update -y && \
    apt install build-essential cmake make wget git -y

USER root

WORKDIR /app

# Install ParlAI
RUN git clone https://github.com/facebookresearch/ParlAI.git ~/ParlAI && \
    cd ~/ParlAI; python setup.py develop && \
    cd /app

# Copy the file from your host to your current location.
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY chat.py .

EXPOSE 37456 

CMD ["uvicorn", "chat:app", "--host", "0.0.0.0", "--port","37456"]
