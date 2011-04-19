from fabric.api import *

dev_queue = "50.56.120.205"
test_host = "127.0.0.1:2222"
bee1 = '208.115.204.105'
bee2 = '69.162.107.106'
testbee = 'testbee1.runzhq.com'
env.roledefs = {
    'web': [testbee],
    'queue': [dev_queue],
    'loadbalancer' : bee1,
    'agents' : [bee1,bee2],
    'event_handler' : [bee1,bee2]
}
