from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "etudiants.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Etudiant(Base):
    __tablename__ = "etudiant"

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    adresse = Column(String)
    pincode = Column(String)

def init_db():
    Base.metadata.create_all(engine)
