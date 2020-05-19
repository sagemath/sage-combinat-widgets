FROM sagemath/sagemath:9.1.rc5
USER root
ENV HOME /root
RUN apt-get update && apt-get -qq install -y curl \
    && curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash - \
    && apt-get install -yq nodejs && npm install npm@latest -g
USER sage
ENV HOME /home/sage
RUN sage -pip install --upgrade ipywidgets jupyterlab
COPY --chown=sage:sage . ${HOME}/sage-combinat-widgets
WORKDIR ${HOME}/sage-combinat-widgets
RUN sage -pip install .
RUN sage -jupyter labextension install --no-build @jupyter-widgets/jupyterlab-manager \
 && sage -jupyter lab build \
 && sage -jupyter lab clean
