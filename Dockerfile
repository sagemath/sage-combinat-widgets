FROM sagemath/sagemath
USER root
ENV HOME /root
RUN apt-get update && apt-get -qq install -y curl \
    &&  curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash - \
    && apt-get install -yq nodejs && npm install npm@latest -g
USER sage
ENV HOME /home/sage
COPY --chown=sage:sage . ${HOME}/sage-combinat-widgets
WORKDIR ${HOME}/sage-combinat-widgets
RUN sage -pip install --upgrade ipywidgets
RUN sage -pip install jupyterlab
RUN cd ./js \
 && npm install \
 && jupyter-labextension install . \
 && cd ..
RUN sage -pip install .
RUN jupyter-labextension install --no-build @jupyter-widgets/jupyterlab-manager \
 && sage -n jupyterlab build \
 && sage -n jupyterlab clean
