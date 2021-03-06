from enum import Enum

from PySide2 import QtCore
from numpy import invert


class MapGraphicsObject(QtCore.QObject):
    enabledChanged = QtCore.Signal()
    opacityChanged = QtCore.Signal()
    parentChanged = QtCore.Signal()
    posChanged = QtCore.Signal()
    rotationChanged = QtCore.Signal()
    visibleChanged = QtCore.Signal()
    zValueChanged = QtCore.Signal()
    toolTipChanged = QtCore.Signal(str)
    flagsChanged = QtCore.Signal()
    selectedChanged = QtCore.Signal()
    newObjectGenerated = QtCore.Signal(object)
    redrawRequested = QtCore.Signal()
    keyFocusRequested = QtCore.Signal()

    removeRequested = QtCore.Signal(object)

    class MapGraphicsObjectFlag(Enum):
        ObjectIsMovable = 1
        ObjectIsSelectable = 2
        ObjectIsFocusable = 4

    def __init__(self, sizeIsZoomInvariant=False, parent=None):
        super().__init__()
        self.__enabled = True
        self.__constructed = False
        self.__opacity = 1.0
        self.__pos = QtCore.QPointF(0.0, 0.0)
        self.__rotation = 0.0
        self.__visible = True
        self.__zValue = 0.0
        self.__selected = False
        self.__toolTip = None
        self.__sizeIsZoomInvariant = sizeIsZoomInvariant
        self.__flags = MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value
        self.setParent(parent)

        QtCore.QTimer().singleShot(1, self.setConstructed)

    def enabled(self):
        """return enabled"""
        return self.__enabled

    def opacity(self):
        """return opacity"""
        return self.__opacity

    def rotation(self):
        """return rotation"""
        return self.__rotation

    def visible(self):
        """return visible"""
        return self.__visible

    def zValue(self):
        """return valued of z"""
        return self.__zValue

    def isSelected(self):
        """return whether the object is selected"""
        return self.__selected

    def toolTip(self):
        """return toolTip"""
        return self.__toolTip

    def flags(self):
        """return flags"""
        return self.__flags

    def sizeIsZoomInvariant(self):
        """return Is size zoom invariant"""
        return self.__sizeIsZoomInvariant

    def boundingRect(self):
        pass

    def contains(self, geoPos):
        """checking position inside the area"""
        geoRect = self.boundingRect()
        return geoRect.contains(geoPos)

    def paint(self, painter, option, widget=0):
        pass

    def setParent(self, nParent):
        self.__parent = nParent
        if self.__constructed:
            self.parentChanged.emit()
        else:
            QtCore.QTimer().singleShot(1, self.parentChanged)
            pass

    def setPos(self, nPos):
        if QtCore.QPointF(nPos) == self.__pos:
            return
        self.__pos = nPos

        if self.__constructed:
            self.posChanged.emit()
        else:
            QtCore.QTimer().singleShot(1, self.posChanged)

    def setRotation(self, nRotation):
        if nRotation == self.__rotation:
            return
        self.__rotation = nRotation

        if self.__constructed:
            self.rotationChanged.emit()
        else:
            QtCore.QTimer().singleShot(1, self.rotationChanged)
            pass

    def setVisible(self, nVisible):
        if nVisible == self.__visible:
            return
        self.__visible = nVisible

        if self.__constructed:
            self.visibleChanged.emit()
            pass
        else:
            QtCore.QTimer().singleShot(1, self.visibleChanged)
            pass

    def setLongitude(self, nLongitude):
        self.setPos(QtCore.QPointF(nLongitude, self.__pos.y()))

    def setLatitude(self, nLatitude):
        self.setPos(QtCore.QPointF(self.__pos.x(), nLatitude))

    def setZValue(self, nZValue):
        self.__zValue = nZValue
        if self.__constructed:
            self.zValueChanged.emit()
            pass
        else:
            QtCore.QTimer().singleShot(1, self.zValueChanged)
            pass

    def setSelected(self, sel):
        if self.__selected == sel:
            return
        self.__selected = sel

        if self.__constructed:
            self.selectedChanged.emit()
            pass
        else:
            QtCore.QTimer().singleShot(1, self.selectedChanged)
            pass

    def setToolTip(self, toolTip):
        self.__toolTip = toolTip
        self.toolTipChanged.emit(toolTip)

    def setFlag(self, flag, enabled=True):
        if enabled:
            self.__flags = self.__flags | flag
        else:
            self.__flags = self.__flags & (invert(flag))

        self.flagsChanged.emit()

    def setFlags(self, flags):
        self.__flags = flags

        if self.__constructed:
            self.flagsChanged.emit()
        else:
            QtCore.QTimer().singleShot(1, self.flagsChanged)
            pass

    def contextMenuEvent(self, event):
        event.ignore()

    def itemChange(self, change, value):
        """return value of change"""
        return value

    def keyPressEvent(self, event):
        event.ignore()

    def keyReleaseEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()

    def mousePressEvent(self, event):
        self.removeRequested.emit(self)
        if self.__flags & MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value or self.__flags & MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable.value:
            event.accept()
            if self.__flags & MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable.value:
                self.keyFocusRequested.emit()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()

    def wheelEvent(self, event):
        event.ignore()

    def setConstructed(self):
        self.__constructed = True

    def pos(self):
        """return position"""
        return self.__pos
