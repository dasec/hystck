virt-install --name linux-template \
--ram 4096 \
--vcpus sockets=1,cores=2,threads=1 \
--disk pool=hystck-pool,bus=sata,size=40,format=qcow2 \
--cdrom /home/test/Downloads/ubuntu-19.10-desktop-amd64.iso \
--network network=public \
--network network=private \
--graphics spice,listen=0.0.0.0 \
--noautoconsole \
-v
