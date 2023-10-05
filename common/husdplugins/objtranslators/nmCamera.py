import hou
import husd
from pxr import UsdGeom


class CameraTranslator(husd.objtranslator.Translator):

    def shouldTranslateNode(self):
        return True

    def primType(self):
        return 'Camera'

    def populatePrim(self, prim, referenced_node_prim_paths, force_active):
        super(CameraTranslator, self).populatePrim(prim, referenced_node_prim_paths, force_active)
        cam = UsdGeom.Camera(prim)
        proj = self._node.parm('projection').evalAsString()
        if proj == 'perspective':
            cam.CreateProjectionAttr('perspective')
        elif proj == 'ortho':
            cam.CreateProjectionAttr('orthographic')
        # A few of the parameters need to be converted into 1/10 scene unit space
        stage = prim.GetStage()
        factor = husd.utils.convertFromMillimetersToCameraUnits(stage, 1.0)
        self.populateAttr(cam.CreateFocalLengthAttr(), self._node.parm('focal'),
                          lambda value: value * factor)
        self.populateAttr(cam.CreateFocusDistanceAttr(), self._node.parm('focus'))
        self.populateAttr(cam.CreateFStopAttr(), self._node.parm('fstop'))
        self.populateAttr(cam.CreateShutterOpenAttr(), self._node.parm('shutter'),
                          lambda value: value * -0.5)
        self.populateAttr(cam.CreateShutterCloseAttr(), self._node.parm('shutter'),
                          lambda value: value * 0.5)
        self.populateAttr(cam.CreateClippingRangeAttr(), [self._node.parm('near'), self._node.parm('far')])
        # Aperture is a bit more complicated
        aspect = float(self._node.parm('resy').eval()) / self._node.parm('resx').eval()
        win_size = self._node.parmTuple('winsize').eval()
        if proj == 'perspective':
            # Start by grabbing a few values we'll use to scale the attributes
            aperture = self._node.parm('aperture').eval()
            self.populateAttr(cam.CreateHorizontalApertureAttr(), self._node.parm('aperture'),
                              lambda value: value * factor * win_size[0])
            self.populateAttr(cam.CreateVerticalApertureAttr(), self._node.parm('aperture'),
                              lambda value: value * aspect * factor * win_size[1])
            self.populateAttr(cam.CreateHorizontalApertureOffsetAttr(), self._node.parmTuple('win'),
                              lambda value: value[0] * aperture * factor)
            self.populateAttr(cam.CreateVerticalApertureOffsetAttr(), self._node.parmTuple('win'),
                              lambda value: value[1] * aperture * aspect * factor)
        elif proj == 'ortho':
            # Start by grabbing a few values we'll use to scale the attributes
            sceneToMM = 1000 * hou.scaleToMKS("m1")
            orthowidth = self._node.parm('orthowidth').eval()
            self.populateAttr(cam.CreateHorizontalApertureAttr(), self._node.parm('orthowidth'),
                              lambda value: value * sceneToMM * factor * win_size[0])
            self.populateAttr(cam.CreateVerticalApertureAttr(), self._node.parm('orthowidth'),
                              lambda value: value * aspect * sceneToMM * factor * win_size[1])
            self.populateAttr(cam.CreateHorizontalApertureOffsetAttr(), self._node.parmTuple('win'),
                              lambda value: value[0] * orthowidth * sceneToMM * factor)
            self.populateAttr(cam.CreateVerticalApertureOffsetAttr(), self._node.parmTuple('win'),
                              lambda value: value[1] * orthowidth * sceneToMM * aspect * factor)


def registerTranslators(manager):
    manager.registerTranslator('nmWorkCam::1.0.1', CameraTranslator)
    manager.registerTranslator('nmWorkCam::1.0.2', CameraTranslator)
    manager.registerTranslator('nmWorkCam::1.0.3', CameraTranslator)
    manager.registerTranslator('nmWorkCam::1.0.4', CameraTranslator)
    manager.registerTranslator('nmWorkCam::1.1.0', CameraTranslator)
    