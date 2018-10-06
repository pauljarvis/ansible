application="'${1}.desktop'"
favourites="/com/canonical/unity/launcher/favorites"
dconf write ${favourites} \
  "$(dconf read ${favourites} \
    | sed "s/, ${application}//g" \
    | sed "s/${application}//g" \
    | sed -e "s/]$/, ${application}]/")"

