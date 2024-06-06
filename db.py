import databases
import sqlalchemy

DATABASE_URL = "sqlite:///mydatabase.db"
db = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    'tasks',
    metadata,
    sqlalchemy.Column(
        'task_id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        'title', sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column(
        'description', sqlalchemy.Text(500), nullable=True),
    sqlalchemy.Column(
        'status', sqlalchemy.Boolean, nullable=False),
)

if __name__ == '__main__':
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={'check_same_thread': False})
    metadata.create_all(engine)

