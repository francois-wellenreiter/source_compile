
FROM ${DOCKER_REGISTRY}ubuntu:20.04 AS base


LABEL maintainer Francois WELLENREITER wellen@free.fr \
      description="Optimized for compilation"

USER root
WORKDIR /tmp

RUN apt-get update
RUN apt-get -y dist-upgrade

RUN apt-get -y install htop iotop iftop sysstat

RUN apt-get -y install libnss-wrapper locales
RUN apt-get -y install tar bzip2 zip unzip ca-certificates wget curl
RUN apt-get -y install software-properties-common apt-transport-https

RUN apt-get -y install pkg-config g++ zlib1g-dev bison flex libgnutls28-dev
RUN apt-get -y install libelf-dev bc libssl-dev libpixman-1-dev
RUN apt-get -y install build-essential automake autoconf libtool cmake git bsdmainutils

RUN apt-get -y install clang-tidy clang-format libboost-all-dev libboost-dev
RUN apt-get -y install libmpfr-dev libmpc-dev libgmp-dev
RUN apt-get -y install xsltproc libnl-3-dev libevent-dev

RUN apt-get -y install gtk-doc-tools libxml2-utils
RUN apt-get -y install qtbase5-dev qtbase5-dev-tools flake8

RUN apt-get -y install libglib2.0-dev
RUN apt-get -y install yasm libfuse-dev libwxbase3.0-dev

RUN apt-get -y install python3-pip python3-git
RUN apt-get -y install python3-numpy python3-scipy

RUN apt-get -y install golang

ENV __MVN_OPTS__="--global-settings /code/maven_settings.xml" 
RUN apt-get -y install maven

ENV __SBT_OPTS__="-Dsbt.global.base=/root/.sbt -Dsbt.ivy.home=/root/.ivy2"
RUN wget https://github.com/bazelbuild/bazel/releases/download/1.1.0/bazel-1.1.0-installer-linux-x86_64.sh && \
  chmod +x bazel-1.1.0-installer-linux-x86_64.sh && \
  ./bazel-1.1.0-installer-linux-x86_64.sh && \
  rm -f bazel-1.1.0-installer-linux-x86_64.sh

RUN wget https://dl.bintray.com/sbt/debian/sbt-1.3.3.deb && \
  dpkg -i ./sbt-1.3.3.deb && \
  rm -f sbt-1.3.3.deb

RUN pip3 install --upgrade scikit-build
RUN pip3 install --upgrade setuptools cmake cffi typing
RUN pip3 install --upgrade pyyaml networkx future pytest pybind11 requests

FROM base AS libc

RUN apt-get -y autoremove
RUN apt-get autoclean
RUN rm -rf /var/cache/apt /var/lib/apt

VOLUME ["/src"]
WORKDIR /src

CMD [ "python3","/code/compile.py", "-U", "-B", "-C" ]




FROM base AS cuda

LABEL maintainer Francois WELLENREITER wellen@free.fr \
      description="Optimized for CUDA compilation"

ENV _COMPILE_FOR_CUDA_ 1

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub && \
  add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /" && \
  apt-get update && \
  apt-get -y install cuda

RUN apt-get -y autoremove
RUN apt-get autoclean
RUN rm -rf /var/cache/apt /var/lib/apt


VOLUME ["/src"]
WORKDIR /src

CMD [ "python3","/code/compile.py", "-U", "-B", "-C" ]


