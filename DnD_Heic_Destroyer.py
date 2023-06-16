import os
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

class DragDropConverter(QtWidgets.QWidget):
    def __init__(self):
        super(DragDropConverter, self).__init__()

        self.setWindowTitle('Drag and Drop Image Converter')
        self.resize(500, 500)

        layout = QtWidgets.QVBoxLayout()
        info_label = QtWidgets.QLabel("Drag your image files here to convert:")
        layout.addWidget(info_label)
        self.setLayout(layout)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.convert_image(file_path)

    def convert_image(self, file_path):
        filename = os.path.basename(file_path)

        if filename.lower().endswith((".jpg", ".jpeg", ".jfif", ".webp", ".heic")):
            with Image.open(file_path) as img:
                img = img.convert("RGB")

                if filename.lower().endswith((".jpg", ".jpeg")):
                    new_filename = filename
                else:
                    new_filename = os.path.splitext(filename)[0] + ".jpeg"

                new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
                img.save(new_file_path, "JPEG")

                if filename.lower().endswith((".webp", ".jfif", ".heic")):
                    os.remove(file_path)

                self.show_conversion_status(file_path, new_file_path)
        else:
            self.show_conversion_status(file_path, None)

    def show_conversion_status(self, original_path, converted_path):
        status_label = QtWidgets.QLabel()
        if converted_path:
            status_label.setText(f"Converted {original_path} to {converted_path}")
        else:
            status_label.setText(f"Unable to convert {original_path}")
        layout = self.layout()
        layout.addWidget(status_label)


app = QtWidgets.QApplication(sys.argv)
converter = DragDropConverter()
converter.show()
sys.exit(app.exec_())
