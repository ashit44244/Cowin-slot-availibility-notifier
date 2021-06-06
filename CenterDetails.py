#!/usr/bin/env python3
from typing import Type


class CenterInfo():

    def __init__(self, name = None, blockname = None, district = None,  pincode = None,  feeType = None,
     capacity = None, dose1 = None, dose2 = None, sessionId = None, vaccine = None, ageLimit = None, date = None):
       self.name = name
       self.blockName = blockname
       self.district = district
       self.pincode = pincode
       self.feeType = feeType
       self.capacity = capacity
       self.dose1 = dose1
       self.dose2 = dose2
       self.sessionId = sessionId
       self.vaccine = vaccine
       self.ageLimit = ageLimit
       self.date = date
     

    def output(self):
        print("Name:", self.name)
        print("block Name: " , self.blockName)
        print("district Id: ", self.district)
        print("pincode: " , self.pincode)
        print("fee Type: " , self.feeType)
        print("capacity: " , self.capacity)
        print("dose 1: " , self.dose1)
        print("dose 2: ",  self.dose2)
        print("sessionId", self.sessionId)
        print("vaccine: " , self.vaccine)
        print("age limit: " , self.ageLimit)
        print("date:" , self.date)
        print("\n")

    def __eq__(self, other):
        if isinstance(other, CenterInfo):

            return self.name + self.sessionId == other.name + other.sessionId

        return False

    def __str__(self) -> str:
        return super().__str__()

    def __hash__(self) -> int:
        return super().__hash__()



#centerInfo = CenterInfo("R C Pura UPHC", "blockname", "urban", "5555", "paid", 100 , 20,30, "", "Covaccine", 18, "19-05-2021")
#centerInfo.output()
