"""
Example of how to upward continue gravity data using the analytical formula
"""
from matplotlib import pyplot
from fatiando import gridder, potential, vis, logger, utils
from fatiando.mesher.volume import Prism3D

log = logger.get()
log.info(logger.header())
log.info("Example of upward continuation using the analytical formula")

height = 100
log.info("Generating synthetic data at %g m:" % (height))
prisms = [Prism3D(-3000,-2000,-3000,-2000,500,2000,{'density':1000}),
          Prism3D(-1000,1000,-1000,1000,0,2000,{'density':-800}),
          Prism3D(1000,3000,2000,3000,0,1000,{'density':500})]
area = (-5000, 5000, -5000, 5000)
shape = (100, 100)
xp, yp, zp = gridder.regular(area, shape, z=-height)
gz = utils.contaminate(potential.prism.gz(xp, yp, zp, prisms), 0.5)

step = 2000
log.info("Upward continuing to %g m" % (height + step))
nodes = (xp, yp, zp)
dims = gridder.spacing(area,shape)
gzcont = potential.transform.upcontinue(step, gz, nodes, dims)

log.info("Computing true values at new height")
gztrue = potential.prism.gz(xp, yp, zp - step, prisms)

pyplot.figure()
pyplot.title("Original")
pyplot.axis('scaled')
vis.contourf(xp, yp, gz, shape, 15)
pyplot.colorbar()

pyplot.figure()
pyplot.title("Continued + true")
pyplot.axis('scaled')
levels = vis.contour(xp, yp, gzcont, shape, 12, color='b', label='continued')
vis.contour(xp, yp, gztrue, shape, levels, color='r', label='true')
pyplot.legend()

pyplot.show()