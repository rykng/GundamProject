import random

class GundamNameGenerator(object):

	PILOTS = ["Char", "Fleming", "Seabook", 
		"Gato", "Shiro", "Kamillie", "Amuro"]


	@classmethod
	def get_randam_pilot_name(cls) -> str:
		outcome:str = random.choice(cls.PILOTS)
		return outcome

