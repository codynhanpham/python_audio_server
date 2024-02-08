# Use Ubuntu Trusty as the base image
FROM ubuntu:trusty

# Update the system and install necessary packages
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    wget \
    libssl-dev \
    zlib1g \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libnss3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    lzma \
    tk-dev \
    libffi-dev \
    portaudio19-dev \
    libasound2-dev \
    llvm \
    git \
    mecab-ipadic-utf8 \
    libsndfile1 \
    gfortran

# https://www.openssl.org/source/openssl-1.0.2u.tar.gz
# Install OpenSSL 1.0.2u
RUN mkdir openssl && \
    cd openssl && \
    wget --no-check-certificate https://www.openssl.org/source/openssl-1.0.2u.tar.gz && \
    tar -xf openssl-1.0.2u.tar.gz && \
    cd openssl-1.0.2u && \
    ./config --prefix=$HOME/openssl --openssldir=$HOME/openssl shared zlib  && \
    make && \
    make && \
    make install

# Set up pyenv
ENV PYTHON_VERSION 3.7.5
RUN apt-get update && apt-get install -y curl
# Set-up necessary Env vars for PyEnv
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Install pyenv
RUN set -ex \
    && curl --insecure https://pyenv.run | bash \
    && pyenv update

# Install Python 3.7 Command
RUN PATH="$HOME/openssl:$PATH"  CPPFLAGS="-I$HOME/openssl/include" CFLAGS="-I$HOME/openssl/include/" LDFLAGS="-L$HOME/openssl/lib -Wl,-rpath,$HOME/openssl/lib" LD_LIBRARY_PATH=$HOME/openssl/lib:$LD_LIBRARY_PATH LD_RUN_PATH="$HOME/openssl/lib" CONFIGURE_OPTS="--with-openssl=$HOME/openssl" PYTHON_CONFIGURE_OPTS="--enable-shared" PYTHON_CFLAGS="-O2" pyenv install $PYTHON_VERSION


# Set the global Python version
RUN pyenv global $PYTHON_VERSION && pyenv rehash

# Upgrade pip and install setuptools and wheel
RUN python3.7 -m pip install --upgrade pip setuptools wheel