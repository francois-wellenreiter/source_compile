
FROM ${DOCKER_REGISTRY}ubuntu:20.04 AS libc


LABEL maintainer Francois WELLENREITER wellen@free.fr \
      description="Optimized for compilation"

USER root

RUN apt-get update
RUN apt-get -y dist-upgrade

RUN apt-get -y install htop iotop iftop sysstat

RUN apt-get -y install locales
RUN apt-get -y install tar bzip2 zip unzip ca-certificates wget curl
RUN apt-get -y install software-properties-common apt-transport-https

RUN apt-get -y install pkg-config g++ zlib1g-dev bison flex libgnutls28-dev
RUN apt-get -y install libelf-dev bc libssl-dev libpixman-1-dev
RUN apt-get -y install build-essential automake autoconf libtool cmake git bsdmainutils patch liblzma-dev

RUN apt-get -y install clang-tidy clang-format libboost-all-dev libboost-dev
RUN apt-get -y install libmpfr-dev libmpc-dev libgmp-dev
RUN apt-get -y install libglib2.0-dev
RUN apt-get -y install xsltproc libnl-3-dev libevent-dev

RUN apt-get -y install gtk-doc-tools libxml2-utils
RUN apt-get -y install qtbase5-dev qtbase5-dev-tools flake8

RUN apt-get -y install python3-pip python3-git
RUN apt-get -y install python3-numpy python3-scipy
RUN apt-get -y install golang-1.14 && \
  cd /usr/bin && rm -f go && ln -s ../lib/go-1.14/bin/go go

RUN pip3 install --upgrade scikit-build
RUN pip3 install --upgrade setuptools cmake cffi typing
RUN pip3 install --upgrade pyyaml networkx future pytest pybind11 requests

RUN cd /tmp && \
  wget https://github.com/bazelbuild/bazel/releases/download/2.0.0/bazel-2.0.0-installer-linux-x86_64.sh && \
  chmod +x bazel-2.0.0-installer-linux-x86_64.sh && \
  ./bazel-2.0.0-installer-linux-x86_64.sh && \
  rm -f bazel-2.0.0-installer-linux-x86_64.sh

RUN apt-get -y autoremove
RUN apt-get autoclean
RUN rm -rf /var/cache/apt /var/lib/apt

VOLUME ["/src"]
WORKDIR /src



