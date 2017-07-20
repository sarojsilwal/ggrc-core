FROM phusion/baseimage

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash - \
  && apt-get update \
  && apt-get install -y \
    curl \
    fabric \
    git-core \
    libfontconfig \
    make \
    mysql-client \
    nodejs \
    python-imaging \
    python-mysqldb \
    python-pip \
    python-pycurl \
    python-virtualenv \
    unzip \
    vim \
    wget \
    zip \
  && rm -rf /var/lib/apt/lists/*

COPY ./provision/docker/vagrant.bashrc /root/.bashrc
COPY ./git_hooks/post-checkout /home/vagrant/.git/hooks/post-checkout
COPY ./git_hooks/post-merge /home/vagrant/.git/hooks/post-merge
WORKDIR /vagrant

# Javascript dependencies
COPY ./package.json ./bower.json /vagrant-dev/
RUN cd /vagrant-dev \
  && npm install \
  && node_modules/.bin/bower --allow-root install

# Python packages
COPY ./Makefile /vagrant/
COPY ./src/requirements*.txt /vagrant/src/
COPY ./bin/init_env ./bin/setup_linked_packages.py /vagrant/bin/
COPY ./extras /vagrant/extras
RUN make setup_dev DEV_PREFIX=/vagrant-dev \
  && make appengine_sdk DEV_PREFIX=/vagrant-dev \
  && make appengine_packages DEV_PREFIX=/vagrant-dev \
  && rm /vagrant-dev/opt/google-cloud-sdk-154.0.1-linux-x86_64.tar.gz

CMD bash -c 'tail -f bin/init_env'
