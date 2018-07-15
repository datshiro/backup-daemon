import os, time

SOURCE_PATH = os.path.join(os.path.expanduser('~'), 'Downloads/')
DESTINATION_PATH = os.path.join(os.path.expanduser('~'),'test-case/dump')
OUTPUT = "{}-{}.zip".format("backup",time.ctime())
