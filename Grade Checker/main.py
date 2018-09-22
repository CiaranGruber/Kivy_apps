"""
Find your grade according to standard JCU limits

Grade Checker. Created by Ciaran Gruber - 22/09/18
"""

from kivy.app import App
from kivy.lang import Builder


class GradeChecker(App):
    def build(self):
        """
        Build the Kivy GUI
        :return:
        """
        self.title = 'Grade Checker'
        self.root = Builder.load_file('extension_grading.kv')
        return self.root

    def clear_all(self):
        """
        Clear all text
        :return:
        """
        self.root.ids.output_label.text = ''
        self.root.ids.input_grade.text = ''

    def calculate_grade(self):
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


GradeChecker().run()
