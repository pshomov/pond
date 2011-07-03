#!/usr/bin/env python
from porcelan_support import launch


p1 = launch("./spin_store_server.py")
p2 = launch("./spin_queue_server.py")

if p1.wait() == 0 and p2.wait() == 0:
    p3 = launch("./spin_web_server.py")
    p4 = launch("./spin_agent_server.py")
    p5 = launch("./spin_repotracker_server.py")
    exit(p3.wait() or p4.wait() or p5.wait())
exit(2)
