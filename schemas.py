from pydantic import BaseModel

class GymBase(BaseModel):
	name: str
	location: str
	latitude: float
	longitude: float
	rating: float

# makes sure the information is a valid data form

class GymCreate(GymBase):
	pass

class Gym(GymBase):
	id: int


	class Config: 
		orm_mode = True