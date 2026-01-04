import sys
import requests

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


LIGHT_QSS = """
QWidget {
    background-color: #f5f5f5;
    color: #1e1e1e;
    font-size: 14px;
}
QTextBrowser, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-radius: 6px;
    padding: 6px;
}
QPushButton {
    background-color: #e0e0e0;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 15px;
}
QPushButton:hover {
    background-color: #d5d5d5;
}
"""

DARK_QSS = """
QWidget {
    background-color: #121212;
    color: #eaeaea;
    font-size: 14px;
}
QTextBrowser, QPlainTextEdit {
    background-color: #1e1e1e;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 6px;
}
QPushButton {
    background-color: #2b2b2b;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 15px;
}
QPushButton:hover {
    background-color: #3a3a3a;
}
"""



class IngredientCopilot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NutriCoach")
        self.resize(900, 650)

        self.current_theme = "light"


        self.all_suggestions = [
            "Is this safe for kids?",
            "What should I be cautious about?",
            "Is there a healthier alternative?",
        ]
        self.remaining_suggestions = self.all_suggestions.copy()


        self.current_query = None
        self.attached_image_path = None

        # Pages
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.landing_page = self.build_landing_page()
        self.copilot_page = self.build_copilot_page()

        self.stack.addWidget(self.landing_page)
        self.stack.addWidget(self.copilot_page)

        self.set_theme("light")

    def build_landing_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("🥗 Ingredient Co-Pilot")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold;")

        subtitle = QLabel(
            "Understand food ingredients instantly.\n"
            "An AI co-pilot that explains what really matters — clearly and honestly."
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; margin-top: 12px;")

        try_btn = QPushButton("Try it →")
        try_btn.setFixedWidth(200)
        try_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(try_btn, alignment=Qt.AlignCenter)
        layout.addStretch()

        return page

    def build_copilot_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        header = QHBoxLayout()
        title = QLabel("🥗 NutriCoach")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()

        theme_btn = QPushButton("🌞 / 🌙")
        theme_btn.clicked.connect(self.toggle_theme)
        header.addWidget(theme_btn)

        layout.addLayout(header)

        self.chat = QTextBrowser()
        self.chat.setOpenLinks(False)
        self.chat.anchorClicked.connect(self.handle_link_click)
        layout.addWidget(self.chat)

        input_layout = QHBoxLayout()

        attach_btn = QPushButton("📎")
        attach_btn.clicked.connect(self.attach_file)
        input_layout.addWidget(attach_btn)

        self.input_box = QPlainTextEdit()
        self.input_box.setPlaceholderText(
            "Paste ingredients, ask a question, or upload a label…"
        )
        self.input_box.setFixedHeight(80)
        input_layout.addWidget(self.input_box)

        send_btn = QPushButton("Explain")
        send_btn.clicked.connect(self.handle_input)
        input_layout.addWidget(send_btn)

        layout.addLayout(input_layout)

        return page



    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.set_theme(self.current_theme)

    def set_theme(self, mode):
        self.setStyleSheet(DARK_QSS if mode == "dark" else LIGHT_QSS)


    def attach_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Attach ingredient label",
            "",
            "Images (*.png *.jpg *.jpeg)",
        )
        if file_path:
            self.attached_image_path = file_path
            self.chat.append(f"📎 <i>Attached:</i> {file_path}")



    def handle_input(self):
        typed_text = self.input_box.toPlainText().strip()

        if not typed_text and not self.attached_image_path:
            return

        # reset suggestions
        self.remaining_suggestions = self.all_suggestions.copy()


        if typed_text:
            self.current_query = typed_text

        query_text = typed_text if typed_text else "Analyze the ingredient label"

        payload = {
            "query": query_text,
            "image_path": self.attached_image_path,
        }

        self.chat.append(f"<b>You:</b> {typed_text or '[Image Uploaded]'}")
        self.input_box.clear()
        self.attached_image_path = None

        self.send_request(payload)



    def handle_link_click(self, url: QUrl):
        question = url.toString()

        if question in self.remaining_suggestions:
            self.remaining_suggestions.remove(question)

        self.chat.append(
            f"<b>You:</b> {question} "
            f"<span style='color:gray;'>(about {self.current_query})</span>"
        )

        payload = {
            "query": question,
            "parent_query": self.current_query,
        }

        self.send_request(payload)



    def send_request(self, payload):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze/",
                json=payload,
                timeout=20,
            )

            data = response.json()
            buttons_html = self.render_suggestion_links()

            ai_html = f"""
<b>🧠 AI Co-Pilot</b><br><br>

<b>🟡 Summary</b><br>
{data.get("summary", "")}<br><br>

<b>🔍 Details</b><br>
{data.get("details", "")}<br><br>

<b>❓ Uncertainty</b><br>
{data.get("uncertainty", "")}<br><br>

{buttons_html}
<hr>
"""
            self.chat.append(ai_html)

        except Exception as e:
            self.chat.append(
                f"<span style='color:red;'>Backend error: {str(e)}</span>"
            )



    def render_suggestion_links(self):
        if not self.remaining_suggestions:
            return ""

        links = []
        for q in self.remaining_suggestions:
            links.append(
                f'<a href="{q}" '
                f'style="padding:6px 12px; background:#4a90e2; color:white; '
                f'text-decoration:none; border-radius:6px;">{q}</a>'
            )
        return "&nbsp;&nbsp;&nbsp;".join(links)


# -------------------- RUN --------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IngredientCopilot()
    window.show()
    sys.exit(app.exec_())
