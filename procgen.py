import numpy

def generate_map(width, height, maptype="basic"):
    gamemap = numpy.array(width, height, str)
    gamemap.fill(".")
    return gamemap
