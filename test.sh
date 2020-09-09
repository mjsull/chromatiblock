#! /bin/sh
wget https://github.com/mjsull/chromatiblock/releases/download/v0.4.0/simple_demo.zip
unzip simple_demo.zip
chromatiblock  -d simple_demo -w cb_working_dir_simple -o H_pylori.html --keep -l simple_demo/order_list.txt --force
chromatiblock  -d simple_demo -w cb_working_dir_simple -o H_pylori -of all -l simple_demo/order_list.txt -ss --force
sed -i '76764d' H_pylori.pdf
BASEDIR=$(dirname "$0")
sha256sum -c $BASEDIR/sha256