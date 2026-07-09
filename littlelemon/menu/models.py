from django.db import models




class Category(models.Model):

    name = models.CharField(max_length=100, db_index=True) # we put "db_index=True" because we will use this feature in search so it will be fast search
    description = models.TextField(blank=True)

    def __str__(self):

        return self.name



class MenuItems(models.Model):
    """
    Menu model representing menu items
    """

    # on_delete=models.CASCADE means if a Category is deleted, delete its items too.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    
    # NEW IMAGE FIELD (Before Image field run: pip install Pillow)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} - ${self.price}"

    class Meta:
        ordering = ['title']

