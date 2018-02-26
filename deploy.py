
# coding: utf-8

# In[ ]:


import paramiko
import time

def deploy(path_to_ssh_key_private_key, server_address, prefix):
    print "Connecting to box"
    print ""
    k = paramiko.RSAKey.from_private_key_file(path_to_ssh_key_private_key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "connecting"
    c.connect(hostname = server_address, username = "testtest", pkey = k ) # change back username 
    print "connected"

    c.exec_command("rm -rf sprint2; git clone https://github.com/savannahvi/sprint2.git")
    print "Pull from Sprint2 successful"
    time.sleep(8)
    c.exec_command("rm -r /srv/runme/" +prefix)
    c.exec_command("mkdir /srv/runme/" + prefix)
    c.exec_command("")
    c.exec_command("""screen -d -m -s "Flask Server" python ~/sprint2/flasky.py %s"""%prefix)
    c.exec_command("mv ~/sprint2/logrotate.conf  /srv/runme/"+prefix)
    c.exec_command("""(crontab -l ; echo "*/2 * * * * logrotate /srv/runme/prefix/logrotate.conf --state /srv/runme/%s/logrotate-state --verbose --force")| crontab -"""%(prefix))
    print "Script fully executed ... exiting"
    c.close()

    
deploy('/Users/chrispaul/testtest','ec2-54-213-45-43.us-west-2.compute.amazonaws.com','anchor')


