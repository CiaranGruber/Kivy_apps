"""
Allow usage of many different conversions and calculations

Ciaran's Conversions and Calculations. Created by Ciaran Gruber
"""

from kivy.app import App
from kivy.lang import Builder


class ConversionsAndCalculations(App):
    """Representation of the ConversionsAndCalculations Kivy-based class"""

    def build(self):
        self.title = 'Conversions and Calculations'
        self.root = Builder.load_file('title_page.kv')
        return self.root

    def choose_application(self):
        if self.root.ids.chooser.text == 'Uni Grade Checker':
            self.root.ids.grading_popup.open()

    def grade_clear_all(self):
        """
        Clear all text
        :return:
        """
        self.root.ids.output_label.text = ''
        self.root.ids.input_grade.text = ''

    def grade_calculate_grade(self):
        """
        Handle the pressing the greet button
        :return:
        """
        try:
            if int(self.root.ids.input_grade.text) >= 85:
                grade = 'High Distinction'
            elif int(self.root.ids.input_grade.text) >= 75:
                grade = 'Distinction'
            elif int(self.root.ids.input_grade.text) >= 65:
                grade = 'Credit'
            elif int(self.root.ids.input_grade.text) >= 50:
                grade = 'Pass'
            else:
                grade = 'Fail'
            print('Your grade is', grade)
            self.root.ids.output_label.text = 'Grade: ' + grade
        except ValueError:
            print('Invalid Grade')
            self.root.ids.output_label.text = 'Invalid Grade'

    def on_stop(self):
        pass


ConversionsAndCalculations().run()
