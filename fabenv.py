from fabric.api import *

dev_queue = "50.56.120.205"
test_dev = "50.56.123.171"
test_host = "127.0.0.1:2222"
bee1 = '208.115.204.105'
bee2 = '69.162.107.106'
bee3 = '74.63.230.2'
bee4 = '74.63.230.5'
bee5 = '208.115.247.113'
bee6 = '208.115.247.112'
bee7 = '208.115.247.114'
testbee = 'testbee1.runzhq.com'
env.roledefs = {
    'web': [test_dev],
    'queue': dev_queue,
    'repotracker' : [testbee],
    'agents' : [bee1, bee2, bee3, bee4, bee5, bee6, bee7],
    'storage' : [test_dev]
}
