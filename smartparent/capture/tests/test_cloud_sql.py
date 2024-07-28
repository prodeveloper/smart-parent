from unittest import TestCase

from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import pg8000
from smartparent.config import ConfigLoader

class TestCloudSql(TestCase):
    """
    Tests the Cloud SQL connection.
    """
    def test_connect_with_connector(self) -> sqlalchemy.engine.base.Engine:
        """
        Initializes a connection pool for a Cloud SQL instance of PostgreSQL.

        Uses the Cloud SQL Python Connector package.
        """
        #You must run <b> gcloud auth application-default login </b> before this works
        # Note: Saving credentials in environment variables is convenient, but not
        # secure - consider a more secure solution such as
        # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
        # keep secrets safe.

        database_config = ConfigLoader().database_config
        db_user = database_config.DB_USER
        db_pass = database_config.DB_PASSWORD
        db_name = database_config.DB_NAME
        instance_connection_name = database_config.INSTANCE_CONNECTION_NAME
        ip_type = IPTypes.PRIVATE if database_config.IS_PRIVATE is True else IPTypes.PUBLIC
        connector = Connector(ip_type)

        def getconn() -> pg8000.Connection:
            return connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_user,
                password=db_pass,
                db=db_name,
            )

        pool = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
            # ...
        )
        assert pool is not None
        with pool.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT 1"))
            assert result.scalar() == 1