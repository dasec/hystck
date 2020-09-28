# this script will update the hystck framework using a filesystem passthrough via 9p

# clear old files
cd ~
rm -r hystck/
mkdir hystck/

# mount shared folder (from host: /hostshare, to guest: /mnt/guestshare)
sudo mount -t 9p -o trans=virtio,version=9p2000.L /hostshare /mnt/guestshare

# get new files
cp -r /mnt/guestshare/* hystck/
cd hystck/

# update hystck-installation
pip uninstall hystck -y
pip install --user .