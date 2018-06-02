import uuid
from hashlib import sha3_512 as hashing_function


def uploaded_file_path(instance, filename):
    """
    Generates unique path for the uploaded file to be used.
    :param instance: Version object.
    :param filename: Name of the file to be used.
    :return: Path where file should be saved.
    """
    return f'{instance.versioned_object.uuid}/{uuid.uuid4()}_{filename}'


def checksum(file_name, chunk_size=4096):
    """
    Generates checksum for given file.
    :param file_name: Name of the file for which checksum is to be generated.
    :param chunk_size: Size of chunks to be loaded to memory at a time.
    :return: Checksum of the file (check hashing_function is this file).
    """
    file_checksum = hashing_function()
    with open(file_name, 'rb') as file:
        for chunk in iter(lambda: file.read(chunk_size), b''):
            file_checksum.update(chunk)

    return file_checksum


def update_device(ip_address):
    """ Mocks updating device based on the versions in database. """
    print(ip_address)
