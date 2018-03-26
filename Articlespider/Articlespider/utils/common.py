import hashlib


def get_md5(url):
    """

    :param url: string
    :return:string
    """
    url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()



