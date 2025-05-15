#!/usr/bin/env bash
export ITHEMAL_HOME="/shared/data/tanayd2/CS521/Ithemal"
export DYNAMORIO_HOME="/home/aa117/DynamoRIO-Linux-9.93.19524"
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

set -ex

if [[ -z "${ITHEMAL_HOME}" ]]; then
    echo "ITHEMAL_HOME environment variable must be set!"
    exit 1
fi

if [[ -z "${DYNAMORIO_HOME}" ]]; then
    echo "DYNAMORIO_HOME environment variable must be set!"
    exit 1
fi

BUILD_DIR="${ITHEMAL_HOME}/data_collection/build"

if [ ! -d "${BUILD_DIR}" ]; then
    mkdir "${BUILD_DIR}"
fi

cd "${BUILD_DIR}"
cmake -DDynamoRIO_DIR="${DYNAMORIO_HOME}/cmake" -DCMAKE_BUILD_TYPE=Debug ..
make -j"$(nproc --all)"
