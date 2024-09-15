# Question 1: By default are django signals executed synchronously or asynchronously?.
# Answer: # It depends on the sending method like django support both async and sync method and the receiver modified itself in the style of the signal.

# Basically there are two types of methods to send signals
# Signal.send()               # it's synchronous
# Signal.asend()          # it's asynchronous


# Creating a custom signal
import django.dispatch

pizza_done = django.dispatch.Signal()


# Sending this signal synchronously
class PizzaStore:
    ...

    def send_pizza(self, toppings, size):
        pizza_done.send(sender=self.__class__, toppings=toppings, size=size)
        ...


# Sending the signal asynchronously
class PizzaStore:
    ...

    async def asend_pizza(self, toppings, size):
        await pizza_done.asend(sender=self.__class__, toppings=toppings, size=size)
        ... 

# Receiver modified itself in the style of the sending method either sync or async.
# Synchronous receivers will be called using sync_to_async() when invoked via asend(). Asynchronous receivers will be called using async_to_sync() when invoked via sync().


# ---------------------------------------------- Question 2 ------------------------------------------------------
# Question 2: Do django signals run in the same thread as the caller?
# Answer: Yes Django signals run in the same thread for the signals which are send using the Signal.send method like most of the default signals are sent using the Signal.send method so that we can say that they execute in the same thread but if the method is Signal.asend then it can be execute in a different thread.

# the below code will show that the signal is executing in the same thread or not if the thread name is same then it's in the same thread otherwise it is in the different thread.

# In the below case I guess post_save signal is sent using Signal.send method so the execution will also be happened in the same thread.
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def my_signal_receiver(sender, instance, **kwargs):
    print(f"Signal receiver thread: {threading.current_thread().name}")

# Simulate saving a user
print(f"Main thread: {threading.current_thread().name}")
new_user = User(username="test_user")
new_user.save()


# ---------------------------------------------------- Question 3 ------------------------------------------------
# Question 3: By default, do Django signals run in the same database transaction as the caller?
# Answer: Yes, Django signals run in the same database transaction as the caller by default. This means that if the database transaction fails or is rolled back, the signal's changes are also rolled back.


# The below code will show the actual flow for this condition.

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def my_signal_receiver(sender, instance, **kwargs):
    print("Signal received, creating another user inside transaction")
    User.objects.create(username="signal_created_user")

try:
    # all the changes made inside this transcation.atomic block will be rolled back if any excpetion raises
    with transaction.atomic():          # atomic put all changes into a single transcation
        new_user = User(username="test_user")
        new_user.save()
        raise Exception("Simulated error, rollback transaction")
except:
    print("Transaction failed, rolling back")

# Check if 'signal_created_user' was created
if User.objects.filter(username="signal_created_user").exists():
    print("Signal-created user exists in the database")
else:
    print("Signal-created user does not exist in the database")


# As Django signals run in the same transcation so the above code give this output.

# Signal received, creating another user inside transaction
# Transaction failed, rolling back
# Signal-created user does not exist in the database

# And no user is saved in the database.