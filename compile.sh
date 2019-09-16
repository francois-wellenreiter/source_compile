#!/bin/bash

TIMEOUT=${TIMEOUT:-10}
PARALL=${PARALL:-1}
PROCS=${PROCS:-`nproc`}

MVN_OPTS="$MVN_OPTS -T $PROCS"


OBSOLETE_PRODUCT_LIST="\
tensorflow_models tensorflow_benchmarks \
mlperf_inference_policies mlperf_training_policies mlperf_community \
deepbench \
deep500 \
spark mmlspark sparkrdma hibench \
arrow numba \
cudf cuml \
"

PRODUCT_LIST="\
hwloc nccl libfabric numactl \
ompi \
libvirt qemu \
busybox \
linux \
gpi2 \
cpython go \
julia sage scala \
bazel tensorflow mxnet pytorch horovod \
mlperf_inference mlperf_training_results_v0_6 mlperf_training \
scikit_learn \
docker_stacks \
pynn \
bitcoin \
tlaplus \
tor \
youtubedl \
"

product_list=${*:-$PRODUCT_LIST}

function _deploy_void {
return
}

function _clean_void {
return
}

function _compile_void {
return
}


#
# _deploy repositories
#


function _deploy_arrow {
git clone https://github.com/apache/arrow.git -b master arrow
}

function _deploy_bazel {
git clone https://github.com/bazelbuild/bazel.git -b master bazel
}

function _deploy_bitcoin {
git clone https://github.com/bitcoin/bitcoin.git -b master bitcoin
}

function _deploy_busybox {
git clone https://git.busybox.net/busybox -b master busybox
}

function _deploy_cpython {
git clone https://github.com/python/cpython.git -b master cpython
}

function _deploy_cudf {
git clone https://github.com/rapidsai/cudf.git -b master cudf
}

function _deploy_cuml {
git clone https://github.com/rapidsai/cuml.git -b master cuml
}

function _deploy_deep500 {
git clone https://github.com/deep500/deep500.git -b master deep500
}

function _deploy_deepbench {
git clone https://github.com/baidu-research/DeepBench.git -b master deepbench
}

function _deploy_docker_stacks {
git clone https://github.com/jupyter/docker-stacks.git -b master docker_stacks
}

function _deploy_go {
git clone https://github.com/golang/go.git -b master go
}

function _deploy_gpi2 {
git clone https://github.com/cc-hpc-itwm/GPI-2.git -b next gpi2
}

function _deploy_hibench {
git clone https://github.com/intel-hadoop/HiBench.git -b master hibench
}

function _deploy_horovod {
git clone https://github.com/horovod/horovod.git -b master horovod
}

function _deploy_hwloc {
git clone https://github.com/open-mpi/hwloc.git -b master hwloc
}

function _deploy_julia {
git clone https://github.com/JuliaLang/julia.git -b master julia
}

function _deploy_libfabric {
git clone https://github.com/ofiwg/libfabric.git -b master libfabric
}

function _deploy_libvirt {
git clone https://github.com/libvirt/libvirt.git -b master libvirt
}

function _deploy_linux {
git clone https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git -b master linux
}

function _deploy_mlperf_community {
git clone https://github.com/mlperf/community.git -b master mlperf_community
}

function _deploy_mlperf_inference {
git clone https://github.com/mlperf/inference.git -b master mlperf_inference
}

function _deploy_mlperf_inference_policies {
git clone https://github.com/mlperf/inference_policies.git -b master mlperf_inference_policies
}

function _deploy_mlperf_training_results_v0_6 {
git clone https://github.com/mlperf/training_results_v0.6.git -b master mlperf_training_results_v0_6
}

function _deploy_mlperf_training {
git clone https://github.com/mlperf/training.git -b master mlperf_training
}

function _deploy_mlperf_training_policies {
git clone https://github.com/mlperf/training_policies.git -b master mlperf_training_policies
}

function _deploy_mmlspark {
git clone https://github.com/Azure/mmlspark.git -b master
}

function _deploy_mxnet {
git clone https://github.com/apache/incubator-mxnet -b master mxnet
}

function _deploy_nccl {
git clone https://github.com/NVIDIA/nccl.git -b master nccl
}

function _deploy_numactl {
git clone https://github.com/numactl/numactl.git -b master numactl
}

function _deploy_numba {
git clone https://github.com/numba/numba.git -b master numba
}

function _deploy_ompi {
git clone https://github.com/open-mpi/ompi.git -b master ompi
}

function _deploy_pynn {
git clone https://github.com/NeuralEnsemble/PyNN.git -b master pynn
}

function _deploy_pytorch {
git clone https://github.com/pytorch/pytorch.git -b master pytorch
}

function _deploy_qemu {
git clone https://git.qemu.org/git/qemu.git -b master qemu
}

function _deploy_sage {
git clone https://github.com/sagemath/sage.git -b master sage
}

function _deploy_scala {
git clone https://github.com/scala/scala.git -b 2.13.x scala
}

function _deploy_scikit_learn {
git clone https://github.com/scikit-learn/scikit-learn.git -b master scikit_learn
}

function _deploy_spark {
git clone https://github.com/apache/spark.git -b master
}

function _deploy_sparkrdma {
git clone https://github.com/Mellanox/SparkRDMA.git -b master sparkrdma
}

function _deploy_tensorflow {
git clone https://github.com/tensorflow/tensorflow.git -b master tensorflow
}

function _deploy_tensorflow_benchmarks {
git clone https://github.com/tensorflow/benchmarks.git -b master tensorflow_benchmarks
}

function _deploy_tensorflow_models {
git clone https://github.com/tensorflow/models.git -b master tensorflow_models
}

function _deploy_tlaplus {
git clone https://github.com/tlaplus/tlaplus.git -b master tlaplus
}

function _deploy_tor {
git clone https://git.torproject.org/tor.git -b master tor
}

function _deploy_youtubedl {
git clone https://github.com/rg3/youtube-dl.git -b master youtubedl
}


#
# clean products
#

function _clean_arrow {
cd c_glib
make distclean
cd ..
cd cpp
make distclean
cd ..
cd python
make distclean
cd ..
cd go/arrow
make distclean
cd ../..
cd java
mvn $MVN_OPTS clean
cd ..
}

function _clean_bazel {
bazel clean
bazel shutdown
}

function _clean_bitcoin {
make distclean
}

function _clean_busybox {
return
}

function _clean_cpython {
make distclean
}

function _clean_cudf {
return
}

function _clean_cuml {
return
}

function _clean_deep500 {
return
}

function _clean_deepbench {
return
}

function _clean_docker_stacks {
return
}

function _clean_go {
cd src
go clean
cd ..
}

function _clean_gpi2 {
make distclean
}

function _clean_hibench {
mvn clean
}

function _clean_horovod {
return
}

function _clean_hwloc {
make distclean
}

function _clean_julia {
make distclean
}

function _clean_libfabric {
make distclean
}

function _clean_libvirt {
make distclean
}

function _clean_linux {
make mrproper
}

function _clean_mlperf_community {
return
}

function _clean_mlperf_inference {
return
}

function _clean_mlperf_inference_policies {
return
}

function _clean_mlperf_training_results_v0_6 {
return
}

function _clean_mlperf_training {
return
}

function _clean_mlperf_training_policies {
return
}

function _clean_mmlspark {
return
}

function _clean_mxnet {
make clean
}

function _clean_nccl {
make distclean
}

function _clean_numactl {
make distclean
}

function _clean_numba {
return
}

function _clean_ompi {
make distclean
}

function _clean_pynn {
return
}

function _clean_pytorch {
return
}

function _clean_qemu {
make distclean
}

function _clean_sage {
make distclean
}

function _clean_scala {
sbt clean
}

function _clean_scikit_learn {
./setup.py clean
}

function _clean_spark {
./build/mvn clean
}

function _clean_sparkrdma {
mvn clean
}

function _clean_tensorflow {
bazel clean
bazel shutdown
}

function _clean_tensorflow_benchmarks {
return
}

function _clean_tensorflow_models {
return
}

function _clean_tlaplus {
mvn clean
}

function _clean_tor {
return
}

function _clean_youtubedl {
return
}


#
# _compile products
#

function _compile_arrow {
cd c_glib
brew bundle && \
./autogen.sh && \
./configure && \
make
cd ..
cd cpp
cmake . && \
make
cd ..
cd python
cmake . && \
make
cd ..
cd go/arrow
make
cd ../..
cd java
mvn $MVN_OPTS package -Dmaven.test.skip=true -X
cd ..
}

function _compile_bazel {
bazel build //src:bazel
bazel shutdown
}

function _compile_bitcoin {
./autogen.sh && \
./configure --with-incompatible-bdb --disable-wallet && \
make -j$PROCS
}

function _compile_busybox {
return
}

function _compile_cpython {
./configure --enable-optimizations && \
make -j$PROCS
}

function _compile_cudf {
return
}

function _compile_cuml {
return
}

function _compile_deep500 {
return
}

function _compile_deepbench {
return
}

function _compile_docker_stacks {
return
}

function _compile_go {
cd src
./make.bash --no-clean
cd ..
}

function _compile_gpi2 {
make -j$PROCS
}

function _compile_hibench {
mvn $MVN_OPTS package -Dmaven.test.skip=true -X
}

function _compile_horovod {
return
}

function _compile_hwloc {
./autogen.sh && \
./configure && \
make -j$PROCS
}

function _compile_julia {
make -j$PROCS
}

function _compile_libfabric {
./autogen.sh && \
./configure && \
make -j$PROCS
}

function _compile_libvirt {
./autogen.sh && \
./configure && \
make -j$PROCS
}

function _compile_linux {
make defconfig && \
make -j$PROCS
}

function _compile_mlperf_community {
return
}

function _compile_mlperf_inference {
return
}

function _compile_mlperf_training_results_v0_6 {
return
}

function _compile_mlperf_inference_policies {
return
}

function _compile_mlperf_training {
return
}

function _compile_mlperf_training_policies {
return
}

function _compile_mmlspark {
./runme
}

function _compile_mxnet {
make -j$PROCS
}

function _compile_nccl {
make -j$PROCS
}

function _compile_numactl {
./autogen.sh && \
./configure && \
make -j$PROCS
}

function _compile_numba {
python ./setup.py build_ext
}

function _compile_ompi {
./autogen.pl && \
./configure && \
make -j$PROCS
}

function _compile_pynn {
return
}

function _compile_pytorch {
export MAX_JOBS=$PROCS
python setup.py build_ext
unset MAX_JOBS
}

function _compile_qemu {
./configure && \
make -j$PROCS
}

function _compile_sage {
./configure && \
make -j$PROCS
}

function _compile_scala {
sbt package
}

function _compile_scikit_learn {
./setup.py build_ext
}

function _compile_spark {
./build/mvn $MVN_OPTS -DskipTests package -X
}

function _compile_sparkrdma {
mvn $MVN_OPTS -Dmaven.test.skip=true -Dspark.version=2.3.0 package -X
}

function _compile_tensorflow {


if [ a$_COMPILE_FOR_CUDA_ = a1 ] 
then
PYTHON_BIN_PATH=`which python` USE_DEFAULT_PYTHON_LIB_PATH=1 TF_NEED_MPI=0 \
TF_NEED_HDFS=1 TF_NEED_TENSORRT=0 TF_NEED_JEMALLOC=1 TF_NEED_OPENCL_SYCL=0 \
TF_NEED_COMPUTECPP=1 TF_NEED_OPENCL=0 TF_CUDA_CLANG=0 TF_DOWNLOAD_CLANG=0 \
TF_NEED_GCP=1 TF_NEED_AWS=1 TF_NEED_KAFKA=0 TF_ENABLE_XLA=1 TF_NEED_GDR=1 \
TF_NEED_VERBS=0 TF_NEED_CUDA=1 TF_NEED_ROCM=0 CC_OPT_FLAGS="-march=native" \
TF_SET_ANDROID_WORKSPACE=0 \
	./configure && \
bazel build --config=cuda \
    --copt="-O3" --copt="-mfma" --copt="-mavx2" \
    --copt="-march=broadwell" \
    //tensorflow/tools/pip_package:build_pip_package

else
PYTHON_BIN_PATH=`which python` USE_DEFAULT_PYTHON_LIB_PATH=1 TF_NEED_MPI=0 \
TF_NEED_HDFS=1 TF_NEED_TENSORRT=0 TF_NEED_JEMALLOC=1 TF_NEED_OPENCL_SYCL=0 \
TF_NEED_COMPUTECPP=1 TF_NEED_OPENCL=0 TF_CUDA_CLANG=0 TF_DOWNLOAD_CLANG=0 \
TF_NEED_GCP=1 TF_NEED_AWS=1 TF_NEED_KAFKA=0 TF_ENABLE_XLA=1 TF_NEED_GDR=1 \
TF_NEED_VERBS=0 TF_NEED_CUDA=0 TF_NEED_ROCM=0 CC_OPT_FLAGS="-march=native" \
TF_SET_ANDROID_WORKSPACE=0 \
	./configure && \
bazel build --config=opt \
    --copt="-O3" --copt="-mfma" --copt="-mavx2" \
    --copt="-march=broadwell" \
    //tensorflow/tools/pip_package:build_pip_package
fi
bazel shutdown
}

function _compile_tensorflow_benchmarks {
return
}

function _compile_tensorflow_models {
return
}

function _compile_tlaplus {
mvn $MVN_OPTS package -Dmaven.test.skip=true -X
}

function _compile_tor {
sh autogen.sh && \
./configure --disable-asciidoc && \
make && \
make install
}

function _compile_youtubedl {
return
}




#
# MAIN functions
#


function _gather_ {
REMOTE=`git remote -v | grep origin | grep fetch | awk '{ print $2 }'`
BRANCH=`git branch | awk '{print $2}'`
if [ a$DO_CLEAN = a1 ]
then
    git reset --hard HEAD
fi
git fetch origin
if [ a$BRANCH != a ]
then
	git pull origin $BRANCH
fi
git submodule update --init --recursive
if [ a$DO_CLEAN = a1 ]
then
git prune
git gc
fi
}



function __deploy_and__compile_ {

echo "------------------ $1 $2/$3 -------------------"

if [ ! -d $1 ]
then
	_deploy_$1
fi
cd $1
if [ -z "`git remote 2> /dev/null`" ]
then
	cd ..
	rm -rf $1
	_deploy_$1
else
	cd ..
fi

cd $1
	if [ a$DONT_GATHER != a1 ]
	then
		_gather_
	fi
	if [ a$DO_CLEAN = a1 ]
	then
		_clean_$1
	fi
	if [ a$DONT_COMPILE != a1 ]
	then
		_compile_$1
	fi
cd ..

echo "++++++++++++++++++ $1 $2/$3 +++++++++++++++++++"
}

function _main_ {
cur_nb=0
tot_nb=`echo $* | wc -w`

while [ $# -ge 1 ]
do

	if [ "`pgrep -c -P $$`" -lt "$PARALL" ]
	then
		cur_nb=$((cur_nb+1))
		__deploy_and__compile_ $1 $cur_nb $tot_nb &
		shift
        else
		while [ "`pgrep -c -P$$`" -ge "$PARALL" ]
		do
			sleep $TIMEOUT
		done
	fi

done
}

function main {

_main_ $product_list

while [ `pgrep -c -P$$` -gt "0" ]
do
	sleep $TIMEOUT
done

}

main 2>&1


