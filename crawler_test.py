import pytest
from crawler import *
import hashlib

# copied from https://www.geeksforgeeks.org/compare-two-files-using-hashing-in-python/
def hashfile(file):

    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:

        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def test_parent_child_3_searches():
    # we're only doing 3 crawls for this website
    # ideally we want an internal website we can test that will not change to make sure the program is working
    main("https://rescale.com/", 3)

    f1_hash = hashfile("./test/test_rescale_3_searches.txt")
    f2_hash = hashfile("./website_crawled_results.txt")

    assert f1_hash == f2_hash
