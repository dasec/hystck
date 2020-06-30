path="$1"

poolpath=($(jq -r '.path' config.json))
poolname=($(jq -r '.name' config.json))
publicname=($(jq -r '.public-interface-name' config.json))
privatename=($(jq -r '.private-interface-name' config.json))

if [ "$EUID" -ne 0 ]
    then echo "Script not executed as root"
    exit
fi

if [ ! -f "$path" ]; then
    echo "File not found!"
    exit
fi

virt-install --name windows-template \
--ram 4096 \
--vcpus sockets=1,cores=2,threads=1 \
--disk pool="$poolname",bus=sata,size=40,format=qcow2 \
--cdrom "$path" \
--network network="$publicname" \
--network network="$privatename" \
--graphics spice,listen=0.0.0.0 \
--noautoconsole \
-v \

chown $SUDO_USER "$poolpath"/"$poolname"/windows-template.qcow2
