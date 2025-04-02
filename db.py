
class Connection:
    def __init__(self, users):
        self.users = users
    
    def find_all(self):
        return self.users
    
    def find_user_by_id(self,id):
        for user in self.users:
            if user['id'] == int(id):
                return user
    
        return None
def get_connection():
    return Connection(users)

users = [
    {
      "id":1,
      "name":"John Doe",
      "email":"john.doe@example.com",
      "is_active":True
    },
    {
      "id":2,
      "name":"Frank Kenstan",
      "email":"frank.kenstan@example.com",
      "is_active":True   
    },
    {
      "id":3,
      "name":"Dylan Scooter",
      "email":"dylan.scooter@example.com",
      "is_active":False   
    }  
]