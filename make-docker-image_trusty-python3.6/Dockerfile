# Use Ubuntu Trusty as the base image
FROM ubuntu:trusty

# Update the system and install necessary packages
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    wget \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    libffi-dev \
    portaudio19-dev \
    libasound2-dev \
    git

# Download, compile and install Python 3.6
RUN wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz && \
    tar -xvf Python-3.6.3.tgz && \
    cd Python-3.6.3 && \
    ./configure --enable-optimizations --enable-shared && \
    make && \
    make install

# Install pip
RUN apt-get install -y python3-pip

# Upgrade pip and install setuptools and wheel
RUN pip3 install --upgrade setuptools wheel

# Install PyAudio
RUN apt-get install -y python3-pyaudio

# Install virtualenv
RUN pip3 install virtualenv