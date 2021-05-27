from django.db import models


class Chat(models.Model):
    chat_id = models.CharField(max_length=32)
    is_stats_deliver_ordered = models.BooleanField(default=False, verbose_name='Is stats message needed')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of add bot to chat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Date of update')

    def __str__(self):
        return f"Chat id: {self.chat_id}; stats delivering: {self.is_stats_deliver_ordered}"
