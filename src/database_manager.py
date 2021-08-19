from threading import Lock
import settings
import peewee


class Singleton(object):

    __singleton_instance = None
    __singleton_lock = Lock()

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls, *args, **kwargs):
        Singleton.__singleton_lock.acquire()
        try:
            if cls.__singleton_instance is None:
                cls.__singleton_instance = cls(*args, **kwargs)
        except Exception as e:
            print(f'Error in creating singleton object of class {cls.__name__}, {e}')
        finally:
            Singleton.__singleton_lock.release()
        print("Object created successfully")
        return cls.__singleton_instance

    
class Database(Singleton):

        def __init__(self, name=''):
            Singleton.__init__(self)
            self.db = None
            self.create_data_connection()
        
        def create_data_connection(self):
            print("Going to connect to database...")
            self.db = peewee.MySQLDatabase(
                host=settings.DB_HOST,
                port = settings.DB_PORT,
                user=settings.DB_USERNAME,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME
            )

            if self.db.connect():
                print("Connection created successfully")
            else:
                print("Error in database connection")