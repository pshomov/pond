import time
import openstack.compute
import os
import fabric.api

def image_web_server():
    compute = openstack.compute.Compute(username = os.environ["RACKSPACE_USERNAME"], apikey =os.environ["RACKSPACE_API_KEY"])
    flavour = compute.flavors.find(ram=256)
    images = compute.images.find(name = "Ubuntu 10.10 (maverick)")
    server = compute.servers.create("img-agent", images, flavour)
    serverId = server.id
    rootPass = server.adminPass
    while server.status != u"ACTIVE":
        time.sleep(5)
        server = compute.servers.get(serverId)
        print "status: "+server.status
        print "progress: "+str(server.progress)

    fabric.api.env.password = rootPass
    fabric.api.env.user = 'root'
    fabric.api.env.hosts = [server.public_ip]
