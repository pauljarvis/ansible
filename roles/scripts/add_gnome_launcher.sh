application="${1}.desktop"
favourites_source="/org/gnome/shell/favorite-apps"

favourites_current="$(dconf read ${favourites_source})"
found=$(echo $favourites_current | yq -r '.[] | select(.=="'${application}'")' )

if [ -z "${found}" ] ; then
  dconf write ${favourites_source} \
    "$( dconf read ${favourites_source}  \
      | sed -e "s/]$/, '${application}']/" )"
fi 

