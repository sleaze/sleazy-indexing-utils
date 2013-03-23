import errno, os, re


def fileGetContents(filePath):
    #print filePath
    if not os.path.isfile(filePath):
        return None
    with open(filePath, 'r') as fh:
        return fh.read()

def filePutContents(filePath, data):
    parentPath = dirname(filePath)
    if not os.path.exists(parentPath):
        mkdirs(parentPath)
    with open(filePath, 'wb') as fh:
        fh.write(data)

def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

def dirname(path):
    return os.path.dirname(path)


urlStripper = re.compile(r'^(?:https?:)\/\/([^:\/]+)(?::[0-9]+)?(\/[^?]*)(?:\?.*)?$', re.I)

def urlToLocalFilePath(url):
    print url
    m = urlStripper.match(url)
    if not m:
        print 'No good: %s' % url
    filePath = 'downloads/%s%s' % (m.group(1), m.group(2))
    return filePath

def saveDownloadedFile(url, data):
    filePath = urlToLocalFilePath(url)
    print 'saving url=%s to filePath=%s' % (url, filePath)
    mkdirs(dirname(filePath))
    with open(filePath, 'w') as fh:
        fh.write(data)

def fileAlreadyDownloaded(url):
    filePath = urlToLocalFilePath(url)
    return os.path.exists(filePath)
