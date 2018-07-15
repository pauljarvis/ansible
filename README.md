## ubuntu
#### Pre-Req
- Install Guest Additions

#### Bootstap
```
sudo apt-get install -y python-pip git \
&& sudo pip install ansible \
&& git clone https://github.com/OurFriendIrony/ansible.git /tmp/ansible \
&& cd /tmp/ansible
```

#### Run
`./go.sh -s -p ubuntu -u steve`  

___
## ubuntu-work
#### Prereqs
- Install Guest Additions

#### Bootstap
```
export https_proxy="http://10.0.20.196:8080" \
&& echo -e "Acquire::http::Proxy \"${https_proxy}\";" | sudo tree /etc/apt/apt.conf.d/01proxy > /dev/null \
&& echo -e "[http]\n  ${https_proxy}" > ~/.gitconfig \
&& sudo apt-get install -y python-pip git \
&& sudo -E pip install ansible \
&& git clone https://github.com/OurFriendIrony/ansible.git /tmp/ansible \
&& cd /tmp/ansible
```

#### Run
`./go.sh -s -p ubuntu-work -u steve -t proxy`  
`./go.sh -s -p ubuntu-work -u steve`  

___
## retropie
#### Prereqs
- Connect Wifi
- sudo raspi-config
  - 5 --> 2 [Turn on SSH client]
  - 7 --> 1 [Expand FileSystem]
  
#### Bootstap
```
sudo apt-get install -y python-pip git \
&& sudo pip install ansible \
&& git clone https://github.com/OurFriendIrony/ansible.git /tmp/ansible \
&& cd /tmp/ansible
```

#### Run
`./go.sh -s -p retropie -u steve`  

___
## Help
`./go.sh -h`

___
## Module index
All Modules are documented [**here**](http://docs.ansible.com/ansible/latest/list_of_all_modules.html)
