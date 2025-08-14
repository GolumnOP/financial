import random


# TODO: convert to async task if need
def create_acc_number() -> str:
    return str(random.randint(1000000000, 9999999999))
