import strips

class Battery(object):
	def __init__(self):
		self.container=None

class Flashlight(object):
	def __init__(self, arg):
		self.batteries=[]
		self.cap=None

class Cap(object):
    def __init__(self):
        self.flashlight=None

def On(cap,flashlight):
    return flashlight.cap==cap

def In(battery,flashlight):
	return any([ battery==bat_i 
				for bat_i in flashlight.batteries])

def place_cap(cap,flashlight):
	cap.flashlight=flashlight
	flashlight.cap=cap

def remove_cap(cap,flashlight):
	cap.flashlight=None
	flashlight.cap=None

def insert(battery,flashlight):
	flashlight.batteries.append(flashlight)
	battery.container=flashlight

def make_world():
	instances={"Battery1":Battery(),"Battery2":Battery(),
				"Cap":Cap(),"Flashlight":Flashlight()}
    predicates={"ON":[On,[Cap,Flashlight]],
                "IN":[In,[Battery,Flashlight]]}
