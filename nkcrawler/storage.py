""" storage.py
"""
import logging
import os
import time

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobServiceClient

logger = logging.getLogger()

class AzureStorage():
    """ Azure Storage Tool
    """
    def __init__(self):
        self.container_name = "nkdata"
        self.connection_string = os.getenv("CONNECTION_STRING")

        try:
            # Create the BlobServiceClient object which will be used to create a container client
            self.blob_client = BlobServiceClient.from_connection_string(self.connection_string)
            self.blob_client.max_single_get_size = 128*1024*1024
            self.blob_client.max_single_put_size = 128*1024*1024
            # Create the container
            self.container_client = self.blob_client.get_container_client(self.container_name)
            self.container_client.create_container()
        except ResourceExistsError:
            logger.info("%s is already exists.", self.container_name)
        except Exception as exp:
            raise SystemError('Error') from exp
    
    def load(self, file_name):
        """ load
        """
        try:
            # Instantiate a new BlobClient
            blob_client = self.container_client.get_blob_client(file_name)

            # Download Page Blob
            start = time.perf_counter()
            with open(file_name, "wb") as my_blob:
                download_stream = blob_client.download_blob()
                my_blob.write(download_stream.readall())

            # Output elapsed time
            elapsed_time = time.perf_counter() - start
            logger.info("Complete load file from Azure Blob Storage: %s sec", elapsed_time)
        except ResourceNotFoundError:
            os.remove(file_name)
            logger.info("%s is not Found.", file_name)

    def save(self, file_name):
        """ save
        """
        # Instantiate a new BlobClient
        blob_client = self.container_client.get_blob_client(file_name)

        # Upload the created file
        start = time.perf_counter()
        with open(file_name, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        # Output elapsed time
        elapsed_time = time.perf_counter() - start
        logger.info("Complete load file from Azure Blob Storage: %s sec", elapsed_time)
