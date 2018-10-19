## Summary
The sections below cover the requirements and build steps to get a full functioning linux box meeting whatever requirements you have.
___
## ubuntu
#### Pre-Req
- [If on VM] Install Guest Additions
- Run Bootstrap
- Create a user profile in `user_profiles/` from `user_profile/__DEMO__.yml`. 
  It is referenced with `-u` below.  

#### Run
`./go.sh -s -p ubuntu -u {user_profile}`  

##### Bootstrap
```bash
sudo apt-get install -y python-pip git \
&& sudo pip install ansible \
&& git clone https://github.com/OurFriendIrony/ansible.git /tmp/ansible \
&& cd /tmp/ansible
```

___
## ubuntu-tp
#### Pre-Req
- [If on VM] Install Guest Additions
- Run Bootstrap
- When running the bootstap you will be prompted to enter your windows ntlm password. This is used to get through the rest of the proxies
- Create a user profile in `user_profiles/` from `user_profile/__DEMO__.yml`. 
  It is referenced with `-u` below.  
- Add the generated `PassNTLMv2` to your user profile as `ntlm_pass`

#### First Run
To ensure successful executions, first run the following:
`./go.sh -s -p ubuntu-tp -u {user_profile} -t proxy`  
and then restart you machine before attempting to run the main rollout

#### Run
`./go.sh -s -p ubuntu-tp -u {user_profile}`  


#### Bootstrap
```bash
export https_proxy="http://10.0.20.196:8080" \
&& echo -e "Acquire::http::Proxy \"${https_proxy}\";" | sudo tee /etc/apt/apt.conf.d/01proxy > /dev/null \
&& echo -e "[http]\n  proxy = ${https_proxy}" > ~/.gitconfig \
&& sudo apt-get update \
&& sudo apt-get install -y python-pip git cntlm \
&& sudo -E pip install ansible \
&& git clone https://github.com/OurFriendIrony/ansible.git /tmp/ansible \
&& cd /tmp/ansible \
&& cntlm -H -u ${LOGNAME}@tpplc
```

___
## retropie
#### Pre-Req
- Connect Wifi
- sudo raspi-config
  - 5 --> 2 [Turn on SSH client]
  - 7 --> 1 [Expand FileSystem]

#### Pre-Req [2]
- Create a user profile in `user_profiles/` from `user_profile/__DEMO__.yml`. 
  It is referenced with `-u` below.  

#### Run
`./go.sh -s -p retropie -u {user_profile}`  

#### Bootstrap
```bash
sudo apt-get install -y python-pip git \
&& sudo pip install ansible \
&& git clone https://github.com/OurFriendIrony/ansible.git /tmp/ansible \
&& cd /tmp/ansible
```

___
## Help
`./go.sh -h`

___
## Module index
All Modules are documented [**here**](http://docs.ansible.com/ansible/latest/list_of_all_modules.html)

