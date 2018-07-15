## Summary
The sections below cover the requirements and build steps to get a full functioning linux box meeting whatever requirements you have.
___
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
#### Pre-Run
- Create yourself a profile if you haven't done already in "./profiles/". It is referenced with `-u` below.  

#### Run
`./go.sh -s -p ubuntu -u steve`  

___
## ubuntu-tp
#### Prereqs
- Install Guest Additions
- When running the bootstap you will be prompter to enter your windows ntlm password. This is used to get through the rest of the proxies

#### Bootstap
```
export https_proxy="http://10.0.20.196:8080" \
&& echo -e "Acquire::http::Proxy \"${https_proxy}\";" | sudo tee /etc/apt/apt.conf.d/01proxy > /dev/null \
&& echo -e "[http]\n  ${https_proxy}" > ~/.gitconfig \
&& sudo apt-get install -y python-pip git cntlm \
&& sudo -E pip install ansible \
&& git clone https://github.com/OurFriendIrony/ansible.git /tmp/ansible \
&& cd /tmp/ansible \
&& cntlm -H -u ${LOGNAME}@tpplc
```

#### Pre-Run
- Create yourself a profile if you haven't done already in "./profiles/". It is referenced with `-u` below.  
- Take the PassNTLMv2 you received after running bootstrap and ensure it is put into your profile config.  
- Note that you should run the proxy tag first to make sure all settings are applied before running the rest of the playbook.  

#### Run
`./go.sh -s -p ubuntu-tp -u stest -t proxy`  
`./go.sh -s -p ubuntu-tp -u stest`  

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

#### Pre-Run
- Create yourself a profile if you haven't done already in "./profiles/". It is referenced with `-u` below.  

#### Run
`./go.sh -s -p retropie -u steve`  

___
## Help
`./go.sh -h`

___
## Module index
All Modules are documented [**here**](http://docs.ansible.com/ansible/latest/list_of_all_modules.html)
