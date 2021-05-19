class CenterDetails():
    def __init__(self, name = None, blockname = None, pincode = None,  feeType = None,
     capacity = None, dose1 = None, dose2 = None, vaccine = None, ageLimit = None, date = None):
       self.name = name
       self.blockName = blockname
       self.pincode = pincode
       self.feeType = feeType
       self.capacity = capacity
       self.dose1 = dose1
       self.dose2 = dose2
       self.vaccine = vaccine
       self.ageLimit = ageLimit
       self.date = date
     

    def output(self):
        print("Name:", self.name)
        print("block Name: " , self.blockName)
        print("pincode: " , self.pincode)
        print("fee Type: " , self.feeType)
        print("capacity: " , self.capacity)
        print("dose 1: " , self.dose1)
        print("dose 2: ",  self.dose2)
        print("vaccine: " , self.vaccine)
        print("age limit: " , self.ageLimit)
        print("date:" , self.date)

CenterDetails = CenterDetails("R C Pura UPHC", "blockname", "", "paid", 100 , 20,30, "Covaccine", 18, "19-05-2021")
CenterDetails.output()
