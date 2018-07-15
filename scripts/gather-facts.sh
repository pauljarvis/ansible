#!/bin/bash

source $(pwd)/scripts/setup.sh

#######################################################################

hosts=$( ansible all --list-hosts | awk '{if (NR!=1) {print $1}}' )
for host in ${hosts}; do
  if [ ${host} == "127.0.0.1" ]; then
    connection="-c local"
  else
    connection=""
  fi
  ansible ${host} ${connection} -m setup --tree $(pwd)/.ansible-sys/facts/dist/ -a "filter=*dist*" >> /dev/null
  ansible ${host} ${connection} -m setup --tree $(pwd)/.ansible-sys/facts/all/                     >> /dev/null
done

for fact in $(find $(pwd)/.ansible-sys/facts/ -name "*" -type f); do
  cat "${fact}" | python -m json.tool > "${fact}.bak"
  mv "${fact}.bak" "${fact}"
done

