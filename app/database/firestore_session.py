import sys
from google.cloud import firestore
from app.core.config import settings


if settings.FIRESTORE_EMULATOR_HOST is not None:
    print("using firestore emulator")

if "pytest" in sys.argv[0]:
    from mockfirestore import MockFirestore
    db = MockFirestore()
else:
    db = firestore.Client()


def get_session():
    yield db
