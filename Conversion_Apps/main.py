"""
Allow usage of many different conversions and calculations

Ciaran's Conversions and Calculations. Created by Ciaran Gruber
"""

from operator import itemgetter
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')


class ConversionsAndCalculations(App):
    """Representation of the ConversionsAndCalculations Kivy-based class"""
    currencies = ListProperty()
    home_currency = StringProperty()
    foreign_currency = StringProperty()
    new_foreign_currency = StringProperty()

    def build(self):
        self.title = 'Conversions and Calculations'
        self.root = Builder.load_file('title_page.kv')
        return self.root

    def on_start(self):
        self.currency_data = read_csv('currency_data.txt')
        for _ in range(2):
            del self.currency_data[0]
        self.currencies = [currency[0] for currency in self.currency_data]
        self.home_currency = 'Select'
        self.foreign_currency = 'Select'
        self.new_foreign_currency = 'Select'
        self.converting_currency = False

    def on_pause(self):
        save_csv('currency_data.txt', [['Baseline as Australian Dollar'], ['Name, Acronym, Relative currency']] +
                 self.currency_data)
        return True

    def on_stop(self):
        save_csv('currency_data.txt', [['Baseline as Australian Dollar'], ['Name, Acronym, Relative currency']] +
                 self.currency_data)

    def grade_clear_all(self):
        """
        Clear all text
        :return:
        """
        self.root.ids.grade_output_label.text = ''
        self.root.ids.grade_input_grade.text = ''

    def grade_calculate_grade(self):
        """
        Handle the pressing the greet button
        :return:
        """
        try:
            if int(self.root.ids.grade_input_grade.text) >= 85:
                grade = 'High Distinction'
            elif int(self.root.ids.grade_input_grade.text) >= 75:
                grade = 'Distinction'
            elif int(self.root.ids.grade_input_grade.text) >= 65:
                grade = 'Credit'
            elif int(self.root.ids.grade_input_grade.text) >= 50:
                grade = 'Pass'
            else:
                grade = 'Fail'
            self.root.ids.grade_output_label.text = 'Grade: ' + grade
        except ValueError:

            self.root.ids.grade_output_label.text = 'Invalid Grade'

    def change_celsius(self, amount=0):
        """Change celsius amount"""
        try:
            self.root.ids.celsius_input.text = str(float(self.root.ids.celsius_input.text) + amount)
        except ValueError:
            self.root.ids.celsius_input.text = str(amount)

    def change_fahrenheit(self, amount=0):
        """Change fahrenheit amount"""
        try:
            self.root.ids.fahrenheit_input.text = str(float(self.root.ids.fahrenheit_input.text) + amount)
        except ValueError:
            self.root.ids.fahrenheit_input.text = str(amount)

    def convert_to_fahrenheit(self):
        """Convert celsius to fahrenheit"""
        try:
            self.root.ids.celsius_input.hint_text = 'Enter amount in Celsius'
            self.root.ids.fahrenheit_input.text = '{:.2f}'.format(float(self.root.ids.celsius_input.text)
                                                                  * 9.0 / 5 + 32)
        except ValueError:
            self.root.ids.celsius_input.text = ''
            self.root.ids.celsius_input.hint_text = 'Invalid number'

    def convert_to_celsius(self):
        """Convert fahrenheit to celsius"""
        try:
            self.root.ids.fahrenheit_input.hint_text = 'Enter amount in Fahrenheit'
            self.root.ids.celsius_input.text = '{:.2f}'.format((float(self.root.ids.fahrenheit_input.text) - 32)
                                                               * 5 / 9)
        except ValueError:
            self.root.ids.fahrenheit_input.text = ''
            self.root.ids.fahrenheit_input.hint_text = 'Invalid number'

    def temperature_clear_all(self):
        """Clear temperature values"""
        self.root.ids.celsius_input.text = ''
        self.root.ids.fahrenheit_input.text = ''
        self.root.ids.celsius_input.hint_text = 'Enter amount in Celsius'
        self.root.ids.fahrenheit_input.hint_text = 'Enter amount in Fahrenheit'

    def convert_to_foreign_currency(self):
        """Convert foreign currency from home currency value"""
        if not self.converting_currency:
            self.converting_currency = True
            try:
                self.root.ids.foreign_currency_input.text = '{:.2f}'.format(
                    convert_currency(float(self.root.ids.home_currency_input.text), self.home_currency,
                                     self.foreign_currency, self.currency_data))
            except ValueError:
                pass
        self.converting_currency = False

    def convert_to_home_currency(self):
        """Convert home currency from foreign currency value"""
        if not self.converting_currency:
            self.converting_currency = True
            try:
                self.root.ids.home_currency_input.text = '{:.2f}'.format(
                    convert_currency(float(self.root.ids.foreign_currency_input.text), self.foreign_currency,
                                     self.home_currency, self.currency_data))
            except ValueError:
                pass
        self.converting_currency = False

    def get_currency_values_if_valid(self):
        """
        Fixes any texts for the currency converter if anything is incorrect and returns if it is valid and the
        amounts
        """
        home_value_exists = False
        foreign_value_exists = False
        if self.root.ids.home_currency_input.text == '':
            self.root.ids.home_currency_input.hint_text = 'Must enter an amount before calibrating'
        else:
            home_value_exists = True
        if self.root.ids.foreign_currency_input.text == '':
            self.root.ids.foreign_currency_input.hint_text = 'Must enter an amount before converting'
        else:
            foreign_value_exists = True
        if foreign_value_exists:
            try:
                foreign_amount = float(self.root.ids.foreign_currency_input.text)
                valid_foreign_amount = True
            except ValueError:
                self.root.ids.foreign_currency_input.text = ''
                self.root.ids.foreign_currency_input.hint_text = 'Invalid amount (not a number)'
                foreign_amount = 0
                valid_foreign_amount = False
        else:
            valid_foreign_amount = False
            foreign_amount = 0
        if home_value_exists:
            try:
                home_amount = float(self.root.ids.home_currency_input.text)
                valid_home_amount = True
            except ValueError:
                self.root.ids.home_currency_input.text = ''
                self.root.ids.home_currency_input.hint_text = 'Invalid amount (not a number)'
                home_amount = 0
                valid_home_amount = False
        else:
            valid_home_amount = False
            home_amount = 0

        return home_value_exists is foreign_value_exists is valid_foreign_amount is valid_home_amount is True, \
            home_amount, foreign_amount

    def calibrate_home_currency(self):
        """Calibrate home currency by setting rate to home/foreign text ratio"""
        valid_input, home_amount, foreign_amount = self.get_currency_values_if_valid()
        if valid_input and self.home_currency != 'Select' and self.foreign_currency != 'Select':
            self.currency_data[find_nested_index(self.currency_data, 0, self.home_currency)][1] \
                        = '{:2f}'.format(float(self.currency_data[find_nested_index(self.currency_data, 0,
                                                                                    self.foreign_currency)][1]) *
                                         home_amount / foreign_amount)

    def delete_home_currency(self):
        """Delete the current home currency if selected"""
        if self.home_currency != 'Select':
            self.currencies.remove(self.home_currency)
            del self.currency_data[find_nested_index(self.currency_data, 0, self.home_currency)]
            self.home_currency = 'Select'
            if self.home_currency == self.foreign_currency:
                self.foreign_currency = 'Select'

    def reset_currencies(self):
        """Resets the currencies to the default data"""
        self.currency_data = read_csv('base_currency_data.txt')
        for _ in range(2):
            del self.currency_data[0]
        self.currencies = [currency[0] for currency in self.currency_data]
        self.home_currency = 'Select'
        self.foreign_currency = 'Select'
        self.new_foreign_currency = 'Select'

    def add_currency(self):
        """Add a new currency with error-checking"""
        home_value_exists = False
        foreign_value_exists = False
        if self.root.ids.new_home_currency_input.text == '':
            self.root.ids.new_home_currency_input.hint_text = 'Must enter an amount before calibrating'
        else:
            home_value_exists = True
        if self.root.ids.new_foreign_currency_input.text == '':
            self.root.ids.new_foreign_currency_input.hint_text = 'Must enter an amount before converting'
        else:
            foreign_value_exists = True
        if foreign_value_exists:
            try:
                foreign_amount = float(self.root.ids.new_foreign_currency_input.text)
                self.root.ids.new_foreign_currency_input.hint_text = 'Add value comparatively to home currency'
                valid_foreign_amount = True
            except ValueError:
                self.root.ids.new_foreign_currency_input.text = ''
                self.root.ids.new_foreign_currency_input.hint_text = 'Invalid amount (not a number)'
                foreign_amount = 0
                valid_foreign_amount = False
        else:
            valid_foreign_amount = False
            foreign_amount = 0
        if home_value_exists:
            try:
                home_amount = float(self.root.ids.new_home_currency_input.text)
                self.root.ids.new_home_currency_input.hint_text = 'Add value comparatively to foreign currency'
                valid_home_amount = True
            except ValueError:
                self.root.ids.new_home_currency_input.text = ''
                self.root.ids.new_home_currency_input.hint_text = 'Invalid amount (not a number)'
                home_amount = 0
                valid_home_amount = False
        else:
            valid_home_amount = False
            home_amount = 0
        valid_input = home_value_exists is foreign_value_exists is valid_foreign_amount is valid_home_amount is True
        if self.root.ids.new_home_currency.text == '':
            valid_input = False
            self.root.ids.new_home_currency.hint_text = 'Must enter new currency name'
        elif self.root.ids.new_home_currency.text in self.currencies:
            valid_input = False
            self.root.ids.new_home_currency.text = ''
            self.root.ids.new_home_currency.hint_text = 'Currency already exists'
        else:
            self.root.ids.new_home_currency.hint_text = 'Enter currency name'
        if valid_input and home_amount > 0 and foreign_amount > 0:
            if self.new_foreign_currency != 'Select':
                self.currency_data.append([self.root.ids.new_home_currency.text, str(
                    float(self.currency_data[find_nested_index(self.currency_data, 0, self.new_foreign_currency)][1]) *
                    home_amount / foreign_amount)])
                self.currencies.append(self.root.ids.new_home_currency.text)
                self.root.ids.currency_output_label.text = 'Added currency: ' + self.root.ids.new_home_currency.text
            else:
                self.root.ids.currency_output_label.text = 'Must have a foreign currency'


def on_focus(value):
    return value


def convert_currency(value, home_currency, foreign_currency, currency_data):
    """Convert two currencies"""
    return float(value) * float(currency_data[find_nested_index(currency_data, 0, foreign_currency)][1]) / \
        float(currency_data[find_nested_index(currency_data, 0, home_currency)][1])


def find_nested_index(listing, nested_location, value_to_find):
    """Find the index of a nested list according to a nested location"""
    for index, item in enumerate(listing):
        if item[nested_location] == value_to_find:
            return index
    raise IndexError


def save_csv(filename, save_list):
    """Save a csv from a nested list"""
    with open(filename, mode='w') as csv:
        csv.writelines([','.join(item) + '\n' for item in save_list])


def read_csv(filename):
    """Read a csv and convert to a nested list"""
    with open(filename) as csv:
        return [csv_line.strip().split(',') for csv_line in csv]


if __name__ == '__main__':
    ConversionsAndCalculations().run()
