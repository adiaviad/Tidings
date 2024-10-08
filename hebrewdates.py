from pyluach import dates
from datetime import datetime


class MyDateStr:
    def __init__(self, day: str, month: str, year: str):
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return f'{self.day} {self.month} {self.year}'


class HebrewAndGregorianDate:
    def __init__(self, hebrew: MyDateStr, gregorian: MyDateStr):
        self.hebrew = hebrew
        self.gregorian = gregorian

    def dict(self):
        return {"{{DateHebrewYear}}": self.hebrew.year, "{{DateHebrewDay}}": self.hebrew.day,
                "{{DateHebrewMonth}}": self.hebrew.month,
                "{{DateGregorianYear}}": self.gregorian.year, "{{DateGregorianDay}}": self.gregorian.day,
                "{{DateGregorianMonth}}": self.gregorian.month}


def getGregorianAndJewishDateInHebrew():
    # Set locale to Hebrew to display the month name in Hebrew
    gregorian_to_hebrew_months = {"January": "ינואר", "February": "פברואר", "March": "מרץ", "April": "אפריל",
                                  "May": "מאי", "June": "יוני", "July": "יולי", "August": "אוגוסט",
                                  "September": "ספטמבר", "October": "אוקטובר", "November": "נובמבר",
                                  "December": "דצמבר"}
    # Get the current Gregorian date
    gregorian_date = datetime.now()
    hebrew_date = dates.HebrewDate.today()
    # Get the current Hebrew date
    hebr = MyDateStr(month=hebrew_date.month_name(True), day=hebrew_date.hebrew_day(True),
                     year=hebrew_date.hebrew_year(True, True))
    # Format the Gregorian date in Hebrew (year, month name, day)
    greg = MyDateStr(gregorian_date.strftime('%Y'), gregorian_to_hebrew_months[gregorian_date.strftime('%B')],
                     gregorian_date.strftime('%d'))

    result = HebrewAndGregorianDate(hebrew=hebr, gregorian=greg)
    # Print the dates
    return result
