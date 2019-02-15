set -e
# Only need to change these two variables
PKG_NAME=confil
USER=thoba

OS=$TRAVIS_OS_NAME-64
mkdir ~/conda-bld
wget https://github.com/COMBAT-TB/confil/archive/0.0.1.tar.gz
export SHA=$(sha256sum 0.0.1.tar.gz | awk '{print $1}')
conda config --set anaconda_upload no
export VERSION=`date +%Y.%m.%d`
export CONDA_BLD_PATH=$HOME/miniconda/conda-bld
conda build .
anaconda -t $CONDA_UPLOAD_TOKEN upload -u $USER $CONDA_BLD_PATH/$OS/$PKG_NAME-*.tar.bz2 --force
