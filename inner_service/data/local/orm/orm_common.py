from sqlalchemy.orm import Session

from controller.exceptions_controller import GENERIC_DB_EXCEPTION, BAD_DATA
from data.database import Base


def _commit_changes(db: Session, element: Base, execute: str = "now") -> Base:
    try:
        db.add(element)
    except Exception as e:
        print(e)
        raise BAD_DATA

    if execute == 'wait':
        pass
    else:
        try:
            db.commit()
            db.refresh(element)
        except Exception as e:
            print(e)
            raise BAD_DATA

    return element
