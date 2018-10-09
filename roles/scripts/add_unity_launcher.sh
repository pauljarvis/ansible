application="${1}.desktop"
favourites_source="/com/canonical/unity/launcher/favorites"

favourites_current="$(dconf read ${favourites_source})"
found=$(echo $favourites_current | yq -r '.[] | select(.=="'${application}'")' )

if [ -z "${found}" ] ; then
  dconf write ${favourites_source} \
    "$( dconf read ${favourites_source}  \
      | sed -e "s/]$/, '${application}']/" )"
fi 

