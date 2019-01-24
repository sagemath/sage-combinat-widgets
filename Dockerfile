FROM sagemath/sagemath:8.3
RUN apt-get -qq install -y curl \
    &&  curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash - \
    && apt-get install -yq nodejs && npm install npm@latest -g
COPY --chown=sage:sage . ${HOME}/sage-combinat-widgets
WORKDIR ${HOME}/sage-combinat-widgets
RUN sage -pip install .
