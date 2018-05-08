#!/bin/bash

source ./scripts/setup.sh

#######################################################################
# Functions

usage () {
  PRG=$(basename $0)
  echo "$PRG -p PLAYBOOK [-t TAGS] [-v VERBOSITY] [-k KEY] [-s] [-d] [-h]"
  echo "     -a PLAYBBOOK     path to playbook"
  echo "     -t TAGS          run only tasks with provided tags"
  echo "     -z SKIP          skips tasks with provided tags"
  echo "     -v VERBOSITY     v, vv, vvv, vvvv"
  echo "     -k KEY           use private key"
  echo "     -s               run as sudo"
  echo "     -d               show diffs"
  echo "     -h               show help"
  exit 0
}

get_playbook () {
  playbook="playbooks/${1}.yml"
  echo $playbook
}

#######################################################################
# Get Input

while getopts ":p:t:z:v:k:dsh" arg; do
  case $arg in
    p)
      playbook=$(get_playbook "${OPTARG}")
      ;;
    t)
      tags="--tags \"${OPTARG}\""
      ;;
    z)
      skip="--skip-tags \"${OPTARG}\""
      ;;
    v)
      verbosity="-${OPTARG}"
      ;;
    k)
      key="--private-key \"${OPTARG}\""
      ;;
    d)
      diff="--diff"
      ;;
    s)
      sudo="--ask-become-pass"
      ;;
    h)
      usage
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Check mandatory fields
mandatory_fields=( "playbook" )
mandatory_fields_set=true
for arg in ${mandatory_fields[@]}; do
  if [ -z "${!arg}" ]; then
    echo "Missing argument: ${arg^^}"
    mandatory_fields_set=false
  fi
done
if [ ${mandatory_fields_set} = false ]; then
  usage
  exit 1
fi

# Check playbook exists
if [ ! -f ${playbook} ]; then
  echo "'${playbook}' does not exist"
  exit 1
fi

#######################################################################

exe="ansible-playbook ${playbook} ${tags} ${skip} ${verbosity} ${diff} ${sudo} ${key}"
echo "${exe}"
eval "${exe}"

rm "$(find . -type f -name "*.retry")" 2> /dev/null

