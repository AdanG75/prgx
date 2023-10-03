from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.settings import settings

DATABASE_MAIN_URL = settings.get_database_url()
DATABASE_TEST_URL = settings.get_database_url(test_db=True)

main_engine = create_engine(DATABASE_MAIN_URL)
test_engine = create_engine(DATABASE_TEST_URL)

MainSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=main_engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# It is used to create Models
Base = declarative_base()


def get_db(test: bool = False):
    """
    Provide the DB instance
    :return: The DB instance
    """
    if not test:
        print("**** MAIN ****")
        db = MainSessionLocal()
    else:
        print("**** TEST ****")
        db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()
