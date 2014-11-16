import logging; logger = logging.getLogger("morse." + __name__)
import morse.core.actuator
from morse.core.services import service
from morse.core import mathutils
from morse.helpers.components import add_data
from morse.helpers.transformation import Transformation3d

class PositionBox(morse.core.actuator.Actuator):
    """ 
    This actuator scales and teleports the position box of the 
    robot to the absolute position with respect to the origin 
    of the Blender coordinate reference.

    This box can be used to draw the estimated position of the
    robot, calculated by itself with interval analysis algorithms.

    .. note::
        Coordinates are given with respect to the origin of
        Blender's coordinate axis.
    """

    _name = "Position Box"
    _short_desc = "Motion controller which changes instantly \
                    position box scale and pose"

    add_data('posbox_x', 'initial box X position', "float",
              "X coordinate of the destination, in meter")
    add_data('posbox_y', 'initial box Y position', "float",
              "Y coordinate of the destination, in meter")
    add_data('posbox_z', 'initial box Z position', "float",
             "Z coordinate of the destination, in meter")
    add_data('posbox_l', 'Initial robot length', "float",
             'Scale of the box along Z axis, in radian')
    add_data('posbox_w', 'Initial robot width', "float",
             'Scale of the box along Y axis, in radian')
    add_data('posbox_h', 'Initial box height', "float",
             'Scale of the box along X axis, in radian')

    def __init__(self, obj, parent=None):
        logger.info('%s initialization' % obj.name)
        # Call the constructor of the parent class
        morse.core.actuator.Actuator.__init__(self, obj, parent)

        pose3d = self.position_3d

        self.local_data['posbox_x'] = pose3d.x
        self.local_data['posbox_y'] = pose3d.y
        self.local_data['posbox_z'] = pose3d.z
        self.local_data['posbox_l'] = 1.0
        self.local_data['posbox_w'] = 1.0
        self.local_data['posbox_h'] = 1.0

        logger.info('Component initialized')

    @service
    def pose(self, x=0.0, y=0.0, z=0.0):
        """
        Places the actuator owner's box by the given (x,y,z) vector.

        This is a **absolute** displacement.

        :param x: (default: 0.0) X position, in meter
        :param y: (default: 0.0) Y position, in meter
        :param z: (default: 0.0) Z position, in meter
        """
        self.local_data['posbox_x'] = x
        self.local_data['posbox_y'] = y
        self.local_data['posbox_z'] = z

    @service
    def scale(self, length=1.0, width=1.0, height=1.0):
        """
        Scales the actuator owner's box by the given (length,width,height).

        :param length: (default: 1.0) scale of the box along X axis
        :param width: (default: 1.0) scale of the box along Y axis
        :param height: (default: 1.0) scale of the box along Z axis
        """
        self.local_data['posbox_l'] = length
        self.local_data['posbox_w'] = width
        self.local_data['posbox_h'] = height

    def default_action(self):
        """ Change the position box pose and scale. """
        self.robot_parent.update_position_box(
                (self.local_data['posbox_x'], 
                    self.local_data['posbox_y'], 
                    self.local_data['posbox_z']),
                (self.local_data['posbox_l'],
                    self.local_data['posbox_w'],
                    self.local_data['posbox_h']))