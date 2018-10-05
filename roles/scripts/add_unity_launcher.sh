application="\'${1}.desktop\'"
favourites="com.canonical.Unity.Launcher favorites"
gsettings set ${favourites} \
  "$(gsettings get ${favourites} \
    | sed "s/, *${application} *//g" \
    | sed "s/${application} *, *//g" \
    | sed -e "s/]$/, ${application}]/")"

