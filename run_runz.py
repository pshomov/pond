#!/usr/bin/env python
from porcelan_support import launch


p1 = launch("./new_store_server.py")
p2 = launch("./new_queue_server.py")

if p1.wait() == 0 and p2.wait() == 0:
    p3 = launch("./new_web_server.py")
    p4 = launch("./new_agent_server.py")
    p5 = launch("./new_repotracker_server.py")
    exit(p3.wait() or p4.wait() or p5.wait())
exit(2)
