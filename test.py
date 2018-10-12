import http.client
from base64 import b64encode
import json
import time

class Settings:
  traccar_server='10.65.35.27:8082'
  erpnext_server='10.65.35.117:8000'
  traccar_auth_header={ 'Authorization' : 'Basic %s' % (b64encode(b"admin:admin").decode("ascii")) }
  erpnext_headers = False 

class MeraCurl:
    def curl(method="GET",path="/",body=None):
      conn = http.client.HTTPConnection(Settings.traccar_server)
      conn.request(method, path,headers=Settings.traccar_auth_header,body=body)
      r1 = conn.getresponse()
      body = r1.read().decode('UTF-8')
      print(body) 
  
class Tests:
  def normal():
    MeraCurl.curl("POST","/?id=117%20JN%2017&timestamp="+str(int(time.time()))+"&lat=-20.237403&lon=57.496601&bearing=0&altitude=560.58984300&watertank=100&batt=100&fuelCap=0&fuel=80&speed=0")
    time.sleep(2.5)
    
  def speeding():
    MeraCurl.curl("POST","/?id=900%20MR%2096&timestamp="+str(int(time.time()))+"&lat=-20.237403&lon=57.496601&bearing=0&altitude=560.58984300&watertank=100&batt=100&fuelCap=0&fuel=80&speed=100")
    time.sleep(5)
    Tests.normal()
    pass
  
  def lowWater():
    MeraCurl.curl("POST","/?id=900%20MR%2096&timestamp="+str(int(time.time()))+"&lat=-20.237403&lon=57.496601&bearing=0&altitude=560.58984300&watertank=20&batt=100&fuelCap=0&fuel=80&speed=0")
    time.sleep(5)
    Tests.normal()
    pass

  def lowFuel():
    MeraCurl.curl("POST","/?id=900%20MR%2096&timestamp="+str(int(time.time()))+"&lat=-20.237403&lon=57.496601&bearing=0&altitude=560.58984300&watertank=100&batt=100&fuelCap=0&fuel=20&speed=0")
    time.sleep(5)
    Tests.normal()
    pass
  def distance15000():
    pass
  def openFuelCap():
    MeraCurl.curl("POST","/?id=900%20MR%2096&timestamp="+str(int(time.time()))+"&lat=-20.237403&lon=57.496601&bearing=0&altitude=560.58984300&watertank=100&batt=100&fuelCap=1&fuel=80&speed=0")
    time.sleep(5)
    Tests.normal()
    pass



print(time.time())

#Tests.normal()
Tests.speeding()
Tests.lowWater()
Tests.openFuelCap()
Tests.lowFuel()
