from sqlalchemy.orm import Session
import models, schemas

def get_gyms(db: Session, skip: int = 0, limit: int = 10):
	return db.query(models.Gym).offset(skip).limit(limit).all()
	# grabs data but limits them 

def create_gym(db: Session, gym: schemas.GymCreate):
	db_gym = models.Gym(**gym.dict())
	db.add(db_gym)
	db.commit()
	db.refresh(db_gym)
	return db_gym
# creates instances, commits it to the DB, and returns it with an ID