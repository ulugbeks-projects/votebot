from django.db import models


class BotUser(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    language_code = models.CharField(max_length=10, default='uz')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name


class BotUserChannel(models.Model):
    user = models.OneToOneField(BotUser, on_delete=models.CASCADE)
    channel = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.channel
    

class VoteOptionItem(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vote_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    

class VoteOption(models.Model):
    items = models.ManyToManyField(VoteOptionItem)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 


class VotePost(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, default='none')
    media_id = models.CharField(max_length=255, null=True, blank=True)
    caption = models.TextField()
    message_id = models.CharField(max_length=255, null=True, blank=True)
    options = models.ForeignKey(VoteOption, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption
    

class Vote(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    post = models.ForeignKey(VotePost, on_delete=models.CASCADE)
    option = models.ForeignKey(VoteOptionItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} voted for {self.option} on {self.post}"
    
    class Meta:
        unique_together = ('user', 'post')