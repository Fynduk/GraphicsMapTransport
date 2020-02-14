from ..MapGraphicsObject import MapGraphicsObject
from PySide2.QtGui import QImage
from PySide2.QtCore import QRectF


class MarkObject(MapGraphicsObject):
    def __init__(self, pos, img=0, rot=180, parent=None):
        # TODO zoomLevelChanged marks dont change pos
        super().__init__(True, parent)
        imageList = ['../images/mark0.png', '../images/mark1.png', '../images/mark2.png']
        self.__image = QImage(imageList[img])
        self.__sizeInMeters = QRectF(self.__image.width() / 2, self.__image.height() / 2,
                                     self.__image.width() / 15, self.__image.height() / 15)

        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsMovable.value, True)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsSelectable.value, False)
        self.setFlag(MapGraphicsObject.MapGraphicsObjectFlag.ObjectIsFocusable.value, False)
        self.setMark(pos, self.__sizeInMeters, rot)

    def __del__(self):
        print('Delete MarkObject')

    def boundingRect(self):
        return self.__sizeInMeters

    def paint(self, painter, option, widget=0):
        painter.drawImage(self.__sizeInMeters, self.__image)

    def setMark(self, pos, sizeInMeters, rotation=None):
        width = sizeInMeters.width()
        height = sizeInMeters.height()
        self.__sizeInMeters = QRectF(-0.5 * width,
                                     -0.5 * height,
                                     width, height)
        self.redrawRequested.emit()
        self.setPos(pos)
        if rotation:
            self.setRotation(rotation)

    def mouseMoveEvent(self, event):
        self.redrawRequested.emit()
        self.setPos(event.scenePos())