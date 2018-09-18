"""A dummy module to prevent import errors from Guest.

"""


def default_route(nic=None):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def default_bridge():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def default_network(conn):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def default_connection():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def get_cpu_flags():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def is_pae_capable(conn=None):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def is_hvm_capable():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def is_kqemu_capable():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def is_kvm_capable():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def is_blktap_capable():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def get_default_arch():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def randomMAC(type="xen"):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def randomUUID():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def uuidToString(u):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def uuidFromString(s):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


# the following function quotes from python2.5/uuid.py
def get_host_network_devices():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def get_max_vcpus(conn, type=None):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def get_phy_cpus(conn):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def system(cmd):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def xml_escape(str):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def compareMAC(p, q):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def _xorg_keymap():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def _console_setup_keymap():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def default_keymap():
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def pygrub_path(conn=None):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def uri_split(uri):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def is_uri_remote(uri):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def get_uri_hostname(uri):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def get_uri_transport(uri):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def get_uri_driver(uri):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def is_storage_capable(conn):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def get_xml_path(xml, path=None, func=None):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def lookup_pool_by_path(conn, path):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")


def check_keytable(kt):
    raise RuntimeError("virtinst.utils not loaded. tried to access dummy method")
