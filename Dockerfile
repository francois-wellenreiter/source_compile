

FROM ${DOCKER_REGISTRY}ubuntu:18.04 AS base


LABEL maintainer Francois WELLENREITER wellen@free.fr \
      description="Optimized for compilation"

USER root

RUN apt-get update && \
apt-get -y dist-upgrade && \
apt-get -y install libnss-wrapper locales \
tar bzip2 zip unzip ca-certificates wget curl \
software-properties-common apt-transport-https \
pkg-config g++ zlib1g-dev bison flex libgnutls28-dev \
libelf-dev bc libssl-dev libpixman-1-dev \
htop iotop iftop sysstat \
build-essential automake autoconf libtool cmake git bsdmainutils \
clang-tidy clang-format libboost-all-dev libboost-dev \
golang \
xsltproc libnl-3-dev \
libevent-dev \
gtk-doc-tools \
linuxbrew-wrapper \
libxml2-utils \
qtbase5-dev qtbase5-dev-tools \
flake8 \
libglib2.0-dev \
yasm libfuse-dev libwxbase3.0-dev \
python-pip python-six \
python3-pip \
python3-git \
python3-numpy python3-scipy  \
openjdk-8-jdk maven

RUN cd /tmp && \
wget https://github.com/bazelbuild/bazel/releases/download/1.1.0/bazel-1.1.0-installer-linux-x86_64.sh && \
chmod +x bazel-1.1.0-installer-linux-x86_64.sh  && \
./bazel-1.1.0-installer-linux-x86_64.sh && \
rm -f bazel-1.1.0-installer-linux-x86_64.sh

RUN cd /tmp && \
wget https://dl.bintray.com/sbt/debian/sbt-1.3.3.deb && \
dpkg -i ./sbt-1.3.3.deb && \
rm -f sbt-1.3.3.deb

RUN cd /tmp && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) nightly" && \
apt-get update && \
apt-get -y install docker-ce

RUN pip3 install --upgrade setuptools \
        scikit-build cmake cffi typing \
        pyyaml networkx future pytest pybind11 requests

RUN apt-get -y autoremove && \
apt-get autoclean && \
rm -rf /var/cache/apt

ENV __MVN_OPTS__="--global-settings /code/maven_settings.xml" 
ENV __SBT_OPTS__="-Dsbt.global.base=/home/.sbt -Dsbt.ivy.home=/home/.ivy2"

VOLUME ["/src"]
WORKDIR /src

CMD [ "python3","/code/compile.py", "-U", "-B", "-C" ]




FROM base AS cuda

LABEL maintainer Francois WELLENREITER wellen@free.fr \
      description="Optimized for CUDA compilation"

ENV _COMPILE_FOR_CUDA_ 1

RUN cd /tmp && \
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1810/x86_64/cuda-repo-ubuntu1810_10.1.168-1_amd64.deb && \
apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub && \
add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /" && \
apt-get update && \
apt-get -y install cuda




