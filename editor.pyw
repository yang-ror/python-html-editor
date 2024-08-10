import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QListWidget, QTextEdit, QDialog, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup

def get_py_editable_contents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    py_editable_elements = soup.find_all(lambda tag: tag.has_attr('id') and tag['id'].startswith('py-editable-'))
    return {element['id']: element.get_text(strip=True) for element in py_editable_elements}

def update_py_editable_contents(file_path, updates):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    for key, value in updates.items():
        element = soup.find(id=key)
        if element:
            element.string = value
        else:
            print(f"Warning: Element with id '{key}' not found.")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    print(f"File {file_path} has been updated.")

class EditDialog(QDialog):
    def __init__(self, value):
        super().__init__()
        self.initUI(value)

    def initUI(self, value):
        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setPlainText(value)
        self.textEdit.setMinimumHeight(100)
        layout.addWidget(self.textEdit)

        saveButton = QPushButton('Save')
        saveButton.clicked.connect(self.accept)
        layout.addWidget(saveButton)

        self.setLayout(layout)
        self.setWindowTitle('Edit Content')
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)


    def getText(self):
        return self.textEdit.toPlainText()

class HTMLEditorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.content_dict = {}
        self.file_path = 'index.html'
        self.load_html()

    def initUI(self):
        layout = QVBoxLayout()

        self.load_button = QPushButton('RESET')
        self.load_button.clicked.connect(self.load_html)
        layout.addWidget(self.load_button)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.edit_item)
        layout.addWidget(self.list_widget)

        self.save_button = QPushButton('SAVE')
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.setGeometry(300, 300, 400, 500)
        self.setWindowTitle('HTML Editor')
        self.setMinimumWidth(512)
        self.setMinimumHeight(512)
        self.show()

    def load_html(self):
        # options = QFileDialog.Options()
        # self.file_path, _ = QFileDialog.getOpenFileName(self, "Select HTML File", "", "HTML Files (*.html);;All Files (*)", options=options)
        if self.file_path:
            self.content_dict = get_py_editable_contents(self.file_path)
            self.update_list_widget()

    def update_list_widget(self):
        self.list_widget.clear()
        for value in self.content_dict.values():
            self.list_widget.addItem(value)

    def edit_item(self, item):
        index = self.list_widget.row(item)
        key = list(self.content_dict.keys())[index]
        dialog = EditDialog(self.content_dict[key])
        if dialog.exec_():
            new_text = dialog.getText()
            self.content_dict[key] = new_text
            item.setText(new_text)

    def save_changes(self):
        if self.file_path:
            update_py_editable_contents(self.file_path, self.content_dict)
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Save")
            msg_box.setText("HTML saved successfully")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            print("Changes saved successfully!")
        else:
            print("No file loaded. Please load an HTML file first.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HTMLEditorGUI()
    sys.exit(app.exec_())