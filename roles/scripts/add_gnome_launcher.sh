#!/bin/bash

application="${1}.desktop"
favourites_source="/org/gnome/shell/favorite-apps"

c_init() {
  if [[ -z "$(c_read)" ]]
    then $(c_write "['']"); fi
}
c_read() {
  echo "$( dconf read "${favourites_source}" )"
}
c_write() {
  echo "$( dconf write "${favourites_source}" "${1}" )"
}
already_exists() {
  if [[ "$(c_read)" =~ .*${application}.* ]]
    then echo true; else echo false; fi
}

$(c_init)
favourites_current="$(c_read)"
if ! $(already_exists) ; then
  favourites_new="$( echo $(c_read) | sed -e "s/]$/, '${application}']/" )"
  $(c_write "${favourites_new}")
fi

