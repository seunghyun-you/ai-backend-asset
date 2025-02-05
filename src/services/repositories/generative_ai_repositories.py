from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError

from models.repository_models import User, Base
from services.utils.aws_parameter_store import get_admin_user_information

engine = create_engine('sqlite:///database/generative_ai_application.db')
Session = sessionmaker(bind=engine)

class GenerativeAiRepository:

    def __init__(self, base=Base):
        self.session = Session()
        base.metadata.create_all(engine)

        if self.select_users_total_count_information() == 0:
            self.insert_admin_user_information('/generative_ai_app/user01')
            self.insert_admin_user_information('/generative_ai_app/user02')


    def select_users_total_count_information(self):
        return self.session.query(User).count()
    

    def insert_admin_user_information(self, parameter_store_path):
        user_information = get_admin_user_information(parameter_store_path)
        user = User(**user_information)
        self.session.add(user)
        self.session.commit()


    def select_user_information(self, userid: str):
        try:
            user_information = self.session.query(User).filter(User.userid == userid).one_or_none()
            if user_information:
                return user_information
            else:
                return None
        except (NoResultFound, MultipleResultsFound) as e:
            print(f"Unexpected result: {str(e)}")
            return None
        except SQLAlchemyError as e:
            print(f"Error occurred while querying the database: {str(e)}")
            return None
    