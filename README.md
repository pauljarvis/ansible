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
- Manually configure direct proxy for:
  - apt
  - pip
  - git

#### Bootstap
```
sudo apt-get install -y python-pip git \
&& sudo pip install ansible \
&& git clone https://github.com/OurFriendIrony/ansible.git /tmp/ansible \
&& cd /tmp/ansible
```

#### Run
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
