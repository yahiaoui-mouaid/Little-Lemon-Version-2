from rest_framework import serializers
from django.contrib.auth import get_user_model 


""" New Information in security:
Attack Surface Reduction (The "Principle of Least Privilege"):
The Risk: Using fields = '__all__' exposes everything. 
If you add a hidden internal field later (like is_hidden_from_public), it will automatically be exposed to the API.
The Fix: Never use __all__ for sensitive or write-heavy endpoints. 
Explicitly list what fields the user is allowed to send.
"""

User = get_user_model()

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'email']
        read_only_fields = ['id', 'username']

    # make only the "manager" able to cha,ge users roles
    def validate_role(self, value):
            # 1. Get the current user making the request
            request = self.context.get('request')
            if not request or not request.user:
                raise serializers.ValidationError("Authentication required.")

            # 2. Skip check if it's a new user registration (instance doesn't exist yet)
            if not self.instance:
                return value

            # 3. If the role is actually changing, block it unless they are a MANAGER
            if self.instance.role != value and request.user.role != 'MANAGER':
                raise serializers.ValidationError("Only managers can change user roles.")

            return value
    




