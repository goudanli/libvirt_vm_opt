#!/usr/bin/env python
#_*_ coding:utf8 _*_

import sys
#import xml

try:
    import libvirt
    HAS_LIBVIRT = True
except Exception:
    HAS_LIBVIRT = False


def is_virtual():
    if not HAS_LIBVIRT:
        sys.exit("current system are not support virtual")
    return 'virt'

def get_conn(url):
    if is_virtual() == 'virt':
        try:
            conn = libvirt.open(url)
        except Exception as e:
            sys.exit(e)
    return conn

def close_conn(conn):
    return conn.close()


def list_active_vms(conn):
    vms_list = []
    domain_list = conn.listDomainsID()
    for id in domain_list:
        vminfo = conn.lookupByID(id)
        vms_list.append(vminfo.name())
    return vms_list

def list_inacticve_vms(conn):
    vm_list=[]
    domain_list = conn.listDefinedDomains()
    for id in domain_list:
        vm_list.append(conn.lookupByID(id).name())

    return vm_list

def list_all_vms(conn):
    vms =[]
    vms.extend(list_active_vms(conn))
    vms.extend(list_inacticve_vms(conn))
    return vms

def get_capability(conn):
    capability = conn.getCapabilities()
    return capability

def get_hostname(conn):
    hostname = conn.getHostname()
    return hostname

def get_max_cpus(conn):
    max_cpus = conn.getMaxVcpus(None)
    return max_cpus

def shutdown(conn,vmid):
    vminfo = conn.lookupByID(vmid)
    return vminfo.shutdown()

if __name__ == "__main__":
    url = 'qemu+tcp://192.168.247.18/system'
    conn = get_conn(url)
    for vms in list_all_vms(conn):
        print vms
    print 'max_cpus = %d ' % get_max_cpus(conn)
    print "hostname" + get_hostname(conn)
    """
    vmobj = conn.lookupByName("i-2-8-VM")
    str = open("snapshot.xml").read()
    vmobj.snapshotCreateXML(str)
    """
    """
    poolset = conn.listAllStoragePools()
    for pool in poolset:
        if pool.name() == "718065ba-1b6a-3e53-ac57-3164f18568d3":
            volumes = pool.listAllVolumes()
            for vol in volumes:
                print vol.name() + " " + vol.path()
    """
    close_conn(conn)





