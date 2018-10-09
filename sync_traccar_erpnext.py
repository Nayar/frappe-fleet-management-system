import http.client
from base64 import b64encode
import json

class Settings:
  traccar_server='10.27.21.13:8082'
  erpnext_server='10.27.21.139:8001'
  traccar_auth_header={ 'Authorization' : 'Basic %s' % (b64encode(b"admin:admin").decode("ascii")) }
  erpnext_headers = False
  
class MeraFrappeHelper:
  def curl():
    pass

class Vehicle:
  def getVehiclesFromTraccar():
    conn = http.client.HTTPConnection(Settings.traccar_server)
    
    conn.request("GET", "/api/devices",headers=Settings.traccar_auth_header)
    r1 = conn.getresponse()
    body = r1.read().decode('UTF-8')
    return json.loads(body) 
    pass
  
  def getGroupsFromTraccar():
    conn = http.client.HTTPConnection(Settings.traccar_server)
    
    conn.request("GET", "/api/groups",headers=Settings.traccar_auth_header)
    r1 = conn.getresponse()
    body = r1.read().decode('UTF-8')
    return json.loads(body) 
    pass
  
  def getVehiclesFromErpnext():
    conn = http.client.HTTPConnection(Settings.erpnext_server)
    if(Settings.erpnext_headers == False):
      conn = http.client.HTTPConnection(Settings.erpnext_server)
      conn.request("GET", "/api/method/login?usr=Administrator&pwd=lol", headers={})
      r1 = conn.getresponse()
      headers = r1.getheaders()
      for name,value in headers:
        if (name == 'Set-Cookie' and 'sid' in value):
          Settings.erpnext_headers = {'Cookie': value}
          conn.request("POST", "/api/method/login?usr=Administrator&pwd=lol", headers=Settings.erpnext_headers)
          r1 = conn.getresponse()
          response = r1.read().decode('UTF-8')

    conn.request("GET", '/api/resource/Vehicle',headers=Settings.erpnext_headers)
    r1 = conn.getresponse()
    response = r1.read().decode('UTF-8')
    return json.loads(response)['data']
  def sync_erpnext_traccar():
    erpnext_vehicles = []
    traccar_vehicles = []
    
    for vehicle in Vehicle.getVehiclesFromTraccar():
      traccar_vehicles.append(vehicle['name'])
      if(vehicle['name'] not in erpnext_vehicles):
        #print(vehicle['name'] + ' needs sync')
        pass
    
    for vehicle in Vehicle.getVehiclesFromErpnext():
      erpnext_vehicles.append(vehicle['name'])
      if(vehicle['name'] not in traccar_vehicles):
        print(vehicle['name'] + ' needs sync to traccar')
        conn = http.client.HTTPConnection(Settings.traccar_server)
        Settings.traccar_auth_header['Content-type'] = 'application/json'
        conn.request("POST", "/api/devices",headers=Settings.traccar_auth_header,body='{"uniqueId": "%s", "name" : "%s", "groupId" : 1}' % (vehicle['name'],vehicle['name']))
        r1 = conn.getresponse()
        body = r1.read().decode('UTF-8')
        print(body) 
        pass
class Driver:
  pass

print(Vehicle.getVehiclesFromTraccar())

print()
print()

#Vehicle.getVehiclesFromErpnext()
Vehicle.sync_erpnext_traccar()  
print(Vehicle.getGroupsFromTraccar())
