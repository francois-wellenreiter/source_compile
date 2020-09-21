
FROM ${DOCKER_REGISTRY}ubuntu:20.10 AS libc


LABEL maintainer Francois WELLENREITER wellen@free.fr \
      description="Optimized for compilation"

ENV LANG="en_US.UTF-8"
ENV LC_ALL="en_US.UTF-8"
ENV LANGUAGE="en_US.UTF-8"
ENV TZ="Europe/Paris"
ENV DEBIAN_FRONTEND="noninteractive"

USER root

RUN apt-get update
RUN apt-get -y dist-upgrade

RUN apt-get -y install tar bzip2 zip unzip ca-certificates wget curl \
  software-properties-common apt-transport-https

RUN apt-get -y install pkg-config g++ zlib1g-dev bison flex libgnutls28-dev \
  libelf-dev bc libssl-dev libpixman-1-dev \
  build-essential automake autoconf libtool cmake git bsdmainutils patch \
  liblzma-dev libmpfr-dev libmpc-dev libgmp-dev libglib2.0-dev

RUN apt-get -y install clang-tidy clang-format libboost-all-dev libboost-dev \
  xsltproc libnl-3-dev libevent-dev \
  gtk-doc-tools libxml2-utils \
  qtbase5-dev qtbase5-dev-tools flake8 pandoc

RUN apt-get -y install htop iotop iftop sysstat \
  cloc sloccount cscope

RUN apt-get -y install docker.io

RUN apt-get -y install python3 cython3 \
  python3-pip python3-git python3-six \
  python3-numpy python3-scipy python3-networkx

RUN apt-get install -y golang-1.14 && \
  cd /usr/bin && rm -f go && ln -s ../lib/go-1.14/bin/go go

RUN pip3 install --upgrade scikit-build \
  setuptools cmake cffi typing \
  pyyaml future pytest pybind11 requests

ARG BAZEL_VERSION=3.1.0
RUN cd /tmp && \
  wget https://github.com/bazelbuild/bazel/releases/download/${BAZEL_VERSION}/bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh && \
  chmod +x bazel-3.1.0-installer-linux-x86_64.sh && \
  ./bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh && \
  rm -f bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh

RUN git config --global pull.rebase false && \
    git config --global pull.ff only

RUN apt-get -y autoremove
RUN apt-get autoclean
RUN rm -rf /var/cache/apt /var/lib/apt

VOLUME ["/src"]
WORKDIR /src



