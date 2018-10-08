application="'${1}.desktop'"
favourites="/org/gnome/shell/favorite-apps"
dconf write ${favourites} \
  "$(dconf read ${favourites} \
    | sed "s/, ${application}//g" \
    | sed "s/${application}//g" \
    | sed -e "s/]$/, ${application}]/")"

