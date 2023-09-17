courtMap = {
    "Indoor 1": 1,
    "Indoor 2": 2,
    "Court 1": 3,
    "Court 2": 4,
    "Court 3": 5,
    "Court 4": 6,
    "Court 5": 7,
    "Court 6": 8,
    "Court 7": 9,
    "Court 8": 10,
    "Court 9": 11,
    "Court 10": 12,
    "Court 11": 13,
    "Court 12": 14,
    "Court 13": 15,
    "Court 14": 16,
    "Court 15": 17,
    "Court 16": 18,
    "Court 17": 19,
    "Court 18": 20,
    "Court 19": 21,
    "Court 20": 22,
}

weekdayTimeMap = {
    "5:00 AM": 1,
    "5:30 AM": 2,
    "6:00 AM": 3,
    "6:30 AM": 4,
    "7:00 AM": 5,
    "7:30 AM": 6,
    "8:00 AM": 7,
    "8:30 AM": 8,
    "9:00 AM": 9,
    "9:30 AM": 10,
    "10:00 AM": 11,
    "10:30 AM": 12,
    "11:00 AM": 13,
    "11:30 AM": 14,
    "12:00 PM": 15,
    "12:30 PM": 16,
    "1:00 PM": 17,
    "1:30 PM": 18,
    "2:00 PM": 19,
    "2:30 PM": 20,
    "3:00 PM": 21,
    "3:30 PM": 22,
    "4:00 PM": 23,
    "4:30 PM": 24,
    "5:00 PM": 25,
    "5:30 PM": 26,
    "6:00 PM": 27,
    "6:30 PM": 28,
    "7:00 PM": 29,
    "7:30 PM": 30,
    "8:00 PM": 31,
    "8:30 PM": 32,
    "9:00 PM": 33,
    "9:30 PM": 34,
    "10:00 PM": 35,
}

saturdayTimeMap = {
    "7:00 AM": 1,
    "7:30 AM": 2,
    "8:00 AM": 3,
    "8:30 AM": 4,
    "9:00 AM": 5,
    "9:30 AM": 6,
    "10:00 AM": 7,
    "10:30 AM": 8,
    "11:00 AM": 9,
    "11:30 AM": 10,
    "12:00 PM": 11,
    "12:30 PM": 12,
    "1:00 PM": 13,
    "1:30 PM": 14,
    "2:00 PM": 15,
    "2:30 PM": 16,
    "3:00 PM": 17,
    "3:30 PM": 18,
    "4:00 PM": 19,
    "4:30 PM": 20,
    "5:00 PM": 21,
    "5:30 PM": 22,
    "6:00 PM": 23,
    "6:30 PM": 24,
    "7:00 PM": 25,
    "7:30 PM": 26,
    "8:00 PM": 27,
    "8:30 PM": 28,
    "9:00 PM": 29,
    "9:30 PM": 30,
    "10:00 PM": 31,
}

sundayTimeMap = {
    "8:00 AM": 1,
    "8:30 AM": 2,
    "9:00 AM": 3,
    "9:30 AM": 4,
    "10:00 AM": 5,
    "10:30 AM": 6,
    "11:00 AM": 7,
    "11:30 AM": 8,
    "12:00 PM": 9,
    "12:30 PM": 10,
    "1:00 PM": 11,
    "1:30 PM": 12,
    "2:00 PM": 13,
    "2:30 PM": 14,
    "3:00 PM": 15,
    "3:30 PM": 16,
    "4:00 PM": 17,
    "4:30 PM": 18,
    "5:00 PM": 19,
    "5:30 PM": 20,
    "6:00 PM": 21,
    "6:30 PM": 22,
    "7:00 PM": 23,
    "7:30 PM": 24,
    "8:00 PM": 25,
    "8:30 PM": 26,
    "9:00 PM": 27,
    "9:30 PM": 28,
    "10:00 PM": 29,
}

days = {
    'Monday': weekdayTimeMap,
    'Tuesday': weekdayTimeMap,
    'Wednesday': weekdayTimeMap,
    'Thursday': weekdayTimeMap,
    'Friday': weekdayTimeMap,
    'Saturday': saturdayTimeMap,
    'Sunday': sundayTimeMap,
}

months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
]

dates = []

for i in range(1,32):
    dates.append(str(i))

