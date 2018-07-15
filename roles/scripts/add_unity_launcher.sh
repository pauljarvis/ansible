application="\'${1}.desktop\'"
gsettings set com.canonical.Unity.Launcher favorites "$(gsettings get com.canonical.Unity.Launcher favorites | sed "s/, *${application} *//g" | sed "s/${application} *, *//g" | sed -e "s/]$/, ${application}]/")"

