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
    gfortran \
    libtbb2 \
    libav-tools

# https://ftp.openssl.org/source/openssl-1.1.1q.tar.gz
# Install OpenSSL 1.0.2u
RUN mkdir openssl && \
    cd openssl && \
    wget --no-check-certificate https://ftp.openssl.org/source/openssl-1.1.1q.tar.gz && \
    tar -xf openssl-1.1.1q.tar.gz && \
    cd openssl-1.1.1q && \
    ./config --prefix=$HOME/openssl --openssldir=$HOME/openssl shared zlib  && \
    make && \
    make && \
    make install

# Set up pyenv
ENV PYTHON_VERSION 3.9.18
RUN apt-get update && apt-get install -y curl
# Set-up necessary Env vars for PyEnv
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Install pyenv
RUN set -ex \
    && curl --insecure https://pyenv.run | bash \
    && pyenv update


# Install Python 3.9 Command
RUN PATH="$HOME/openssl:$PATH"  CPPFLAGS="-I$HOME/openssl/include" CFLAGS="-I$HOME/openssl/include/" LDFLAGS="-L$HOME/openssl/lib -Wl,-rpath,$HOME/openssl/lib" LD_LIBRARY_PATH=$HOME/openssl/lib:$LD_LIBRARY_PATH LD_RUN_PATH="$HOME/openssl/lib" CONFIGURE_OPTS="--with-openssl=$HOME/openssl --enable-shared" PYTHON_CONFIGURE_OPTS="--enable-shared" PYTHON_CFLAGS="-O2" pyenv install $PYTHON_VERSION

# Then, install 3.9 dev as well
RUN PATH="$HOME/openssl:$PATH"  CPPFLAGS="-I$HOME/openssl/include" CFLAGS="-I$HOME/openssl/include/" LDFLAGS="-L$HOME/openssl/lib -Wl,-rpath,$HOME/openssl/lib" LD_LIBRARY_PATH=$HOME/openssl/lib:$LD_LIBRARY_PATH LD_RUN_PATH="$HOME/openssl/lib" CONFIGURE_OPTS="--with-openssl=$HOME/openssl --enable-shared" PYTHON_CONFIGURE_OPTS="--enable-shared" PYTHON_CFLAGS="-O2" pyenv install 3.9-dev


# Set the global Python version
RUN pyenv global $PYTHON_VERSION && pyenv rehash

# Upgrade pip and install setuptools and wheel
RUN python3.9 -m pip install --upgrade pip setuptools wheel