from rest_framework import serializers
from .models import MenuItems, Category



class MenuSerializer(serializers.ModelSerializer):

        # Concierge: Show the actual category name, not just a number (ID)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItems
        # fields = '__all__'  # Exposes id, title, price, and inventory (Not secure) 
        fields = ['id', 'category', 'category_name', 'title', 'price', 'inventory', 'image']





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters.")
        return value.strip()



class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name'] # Strictly limit the output to the name



