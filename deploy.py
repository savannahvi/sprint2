
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
    time.sleep(3)
    c.exec_command("rm -r /srv/runme/" +prefix)
    c.exec_command("mkdir /srv/runme/" + prefix)

    c.exec_command("""screen -d -m -s "Flask Server" python ~/sprint2/flasky.py %s"""%prefix)
    c.exec_command(('(crontab -l;'
                   'echo "*/2 * * * * /bin/mv /srv/runme/{0}/Raw.txt /srv/runme/{0}/Raw_\$(date +\%F-\%T)";'
                   'echo "*/2 * * * * /bin/mv /srv/runme/{0}/Proc.txt /srv/runme/{0}/Proc_\$(date +\%F-\%T)")'
                   '| crontab -').format(prefix))
    print "Script fully executed ... exiting"
    c.close()
