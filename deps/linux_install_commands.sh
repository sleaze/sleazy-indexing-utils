#!/usr/bin/env bash

cd "dirname($0)"

sudo aptitude install -y python-dev ipython python-numpy python-libxml2 libxml2-dev libxslt-dev libcurl3 libcurl3-dev libcurl3-openssl-dev
sudo easy_install lxml
sudo easy_install pyquery
sudo easy_install PIL

tar zxvf python-elinks-0.3.tar.gz
cd python-elinks-0.3
python setup.py build
sudo python setup.py install

