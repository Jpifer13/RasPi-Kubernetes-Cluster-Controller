import os
import paramiko

user = environ.get('K8S_USERNAME')
password = environ.get('K8S_PASSWORD')

nodes = {
    'k8s_master': '192.168.1.146'
    'k8s_node00': '192.168.1.149'
    'k8s_node01': '192.168.1.149'
}
