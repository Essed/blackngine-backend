from sqlalchemy import Column, String, Boolean, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    company_users = relationship("CompanyUser", back_populates="company")

class ProccessEmployee(Base):    
    __tablename__ = "proccessemployees"

    id = Column(Integer, primary_key=True)
    proccess_id = Column(Integer, ForeignKey("proccesses.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))

    employee = relationship("Employee", back_populates="proccess_employees")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    lastname = Column(String)
    job_title = Column(String)
    salary = Column(Float(precision=2))

    proccess_employees = relationship("ProccessEmployee", back_populates="employee")
    company_users = relationship("CompanyUser", back_populates="user")


class Proccess(Base):
    __tablename__ = "proccesses"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class CompanyUser(Base):
    __tablename__ = "companyusers"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    user_id = Column(Integer, ForeignKey("employees.id"))

    company = relationship("Company", back_populates="company_users")
    user = relationship("Employee", back_populates="company_users")