virt-install --name windows-template \
--ram 4096 \
--vcpus sockets=1,cores=2,threads=1 \
--disk pool=hystck-pool,bus=sata,size=40,format=qcow2 \
--cdrom /home/test/Downloads/Win10_1909_German_x64.iso \
--network network=public \
--network network=private \
--graphics spice,listen=0.0.0.0 \
--noautoconsole \
-v \

chown $SUDO_USER /data/hystck-pool/windows-template.qcow2
