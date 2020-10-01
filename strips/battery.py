import re
import strips

def make_world():
	S=["On(Cap,Flashlight)"]
	G=[ "On(Cap,Flashlight)",
		"In(Battery1,Flashlight)",
		"In(Battery2,Flashlight)"]
	PlaceCap=[["~On(Cap,Flashlight)"],
				["On(Cap,Flashlight)"]]
	RemoveCap=[["On(Cap,Flashlight)"],
				["~On(Cap,Flashlight)"]]
	Insert1=[["~On(Cap,Flashlight)",
	         "~In(Battery1,Flashlight)" ],
	         ["In(Battery1,Flashlight)"]]
	Insert2=[["~On(Cap,Flashlight)",
	         "~In(Battery2,Flashlight)" ],
	         ["In(Battery2,Flashlight)"]]
	operators=[PlaceCap,Insert1,Insert2,RemoveCap]
	return strips.parse_word(S,G,operators)