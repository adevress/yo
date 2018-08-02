import numpy

def save(filename, *args, **kwargs):
    filename = str(filename)
    if not filename.endswith(".npy"):
        filename += ".npy"
    with open(filename, 'wb') as f:
        numpy.save(f, filename)
        f.flush()

def load(filename, *args, **kwargs):
    try:
        return numpy.load(filename, *args, **kwargs)
    except ValueError as e:
        raise IOError("IOError: while reading %s because %s" % (filename, str(e)))

