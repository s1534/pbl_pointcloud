#FROM nvidia/cuda:10.1-cudnn8-devel-ubuntu18.04
#FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-devel
#FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-devel

FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel

RUN conda install pyg -c pyg -y && conda clean -ya
RUN conda install nodejs "h5py<3.2" jupyterlab ipywidgets tensorboard -c conda-forge -y && conda clean -ya

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
RUN apt-get update
RUN apt-get -y upgrade
#RUN apt-get -y install python3
#RUN apt-get -y install python3-pip
RUN apt-get -y install nano wget curl
RUN apt-get -y install git
RUN apt-get -y install zip
RUN apt-get -y install vim
#RUN apt-get -y install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev

#RUN python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple pillow
#RUN pip3 install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html

#RUN python3 -m pip install --upgrade pip

#RUN pip install --no-cache-dir \
#    black \
#    jupyterlab \
#    jupyterlab_code_formatter \
#    jupyterlab-git \
#   lckr-jupyterlab-variableinspector \
#  jupyterlab_widgets \
#   ipywidgets \
#   import-ipynb \
#   tqdm

# jupyter 起動準備
#RUN jupyter notebook --generate-config
#RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py

#WORKDIR /home