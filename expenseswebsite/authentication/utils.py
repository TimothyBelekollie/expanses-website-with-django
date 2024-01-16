from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
#this class is meant to tell what was generated before has been use.
class AppTokenGenerator(PasswordResetTokenGenerator):
    def __make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+ text_type(user.pk)+text_type(timestamp))
    
    

tokenGenerator=AppTokenGenerator()
        
    