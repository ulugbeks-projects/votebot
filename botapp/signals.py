from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Vote, VoteOptionItem

@receiver(pre_save, sender=Vote)
def update_vote_count(sender, instance, **kwargs):
    """ Handles vote count update when a user changes their vote. """
    if instance.pk:  # If vote already exists (user changing vote)
        old_vote = Vote.objects.get(pk=instance.pk)
        if old_vote.option != instance.option:
            old_vote.option.vote_count -= 1  # Decrease old option count
            old_vote.option.save()

    instance.option.vote_count += 1  # Increase new option count
    instance.option.save()


@receiver(post_delete, sender=Vote)
def decrease_vote_count(sender, instance, **kwargs):
    """ Decreases vote count when a vote is deleted. """
    instance.option.vote_count -= 1
    instance.option.save()
