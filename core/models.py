from django.db import models
from django.contrib.auth.models import User

class ActivityLog(models.Model):
    type = models.CharField(max_length=64)
    logged_user = models.ForeignKey(User, null=True, blank=True)
    fromuser = models.ForeignKey(User, null=True, blank=True, related_name="activitylogs_withfromuser")
    jsondata = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return '%s / %s / %s' % (
            self.type,
            self.logged_user,
            self.created_at,
        )


class Todo(models.Model):
    description = models.CharField(max_length=512)
    done = models.BooleanField(default=False)

    def to_dict_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'done': self.done,
        }


class Personality(models.Model):
    name = models.CharField(max_length=128)
    abstract = models.TextField()

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    question = models.TextField()

    def __str__(self):
        return str(self.id)


class Choice(models.Model):
    choice = models.TextField()
    Personality = models.ForeignKey(
        'Personality',
        on_delete=models.CASCADE,
    )
    Question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
    )
