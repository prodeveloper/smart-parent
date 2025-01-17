from unittest import TestCase

from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import pg8000
import pexpect
import sys
from django.conf import settings
from django.db import connections
from smartparent.config import ConfigLoader
from capture.commands.log_item import LogItem



class TestCloudSql(TestCase):

    """
    Tests the Cloud SQL connection using Django's database configuration.
    """

    def test_django_db_connection(self):
        """
        Tests the connection to Cloud SQL using Django's database configuration.
        """
        # Ensure the database is configured in Django settings
        self.assertIn('google_cloud', settings.DATABASES)

        # Get the default database connection
        connection = connections['google_cloud']
        assert connection is not None

        # Attempt to connect and execute a simple query
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

        # Assert that the query returned the expected result
        LogItem(result).log()
        self.assertEqual(result[0], 1)
    
    def test_cloud_connection(self):
        database_config = ConfigLoader().database_config
        child = pexpect.spawn(
            f"psql -h {database_config.DB_HOST} "
            f"-U {database_config.DB_USER} "
            f"-d {database_config.DB_NAME}"
        )
        try:
            child.expect(f"Password for user {database_config.DB_USER}:")
            child.sendline(database_config.DB_PASSWORD)
            child.expect(f"{database_config.DB_NAME}=>")
            child.sendline("SELECT 1;")
            child.expect(f"{database_config.DB_NAME}=>")
            child.sendline("\\q")
        except pexpect.TIMEOUT as exc:
            raise FailedToConnect("Failed to connect to the database") from exc
        finally:
            child.close()

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

class FailedToConnect(Exception):
    """
    Raised when the connection to the database fails.
    """
    pass