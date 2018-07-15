#!/bin/bash

############################################################################

path_config="$(pwd)/.ansible-sys/ansible.cfg"
path_hosts="$(pwd)/.ansible-sys/hosts"
path_roles="$(pwd)/roles/"

sed -i 's:\(inventory.*=\).*:\1 '"${path_hosts}"':g' ${path_config}
sed -i 's:\(roles_path.*=\).*:\1 '"${path_roles}"':g' ${path_config}

export ANSIBLE_CONFIG="${path_config}"

############################################################################

