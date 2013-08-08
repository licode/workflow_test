from main.models import User

class UserController(object):
    
    def __init__(self):
        #self.user_id = 1
        return
    
    def set_user_data(self, firstname="None", lastname="None"):
        user = User.objects.create(first_name=firstname,
                                   last_name=lastname)
        #self.user_id = user.id
        return user
    
    def get_user(self):
        #assert(len(self.user_id)>0)  ###otherwise it returns admin
        id_val = len(User.objects.all())
        user = User.objects.get(id=id_val-1)
        return user
        
        