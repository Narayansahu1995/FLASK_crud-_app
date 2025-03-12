class School:
    def __init__(self, id,name, address,email):
        self.id = id
        self.name = name
        self.email = email
        self.address = address
    
    def __repr__(self):
        return f"<School {self.id} {self.name} {self.email} {self.address}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address
        }
    