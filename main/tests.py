from django.test import TestCase

# Create your tests here.
import uuid

def short_uuid():
    return uuid.uuid4().hex[:12]

# print(short_uuid())
