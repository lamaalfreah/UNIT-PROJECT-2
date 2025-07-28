from django.db import models

# Create your models here.
class Story(models.Model):
    title = models.CharField(max_length=200)
    child_name = models.CharField(max_length=50)
    topic = models.CharField(max_length=100)
    category = models.CharField(
        max_length=100,
        choices=[
            ('Educational', 'Educational'),
            ('Moral', 'Moral'),
            ('Adventure', 'Adventure')
        ]
    )
    content = models.TextField()
    image = models.ImageField(upload_to='stories/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} – {self.child_name}"

class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="comments")
    full_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.full_name} on {self.story.title}"