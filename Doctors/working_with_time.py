import time
from time import time, ctime
# from Doctors.models import Doctor

days_to_shortcut = {
    "Sunday" : "Sun",
    "Monday" : "Mon",
    "Tuesday" : "Tue",
    "Wednesday" : "Wed",
    "Thrusday" : "Thu",
    "Friday" : "Fri",
    "Saturday" : "Sat",
}

def getDate(time):
    value = str(ctime(time))
    return value[:11] + value[20:24]

def change(day,obj):

    if day == "Sun":
        obj.Sunday = False
        obj.save()
        return
    if day == "Mon":
        obj.Monday = False
        obj.save()
        return
    if day == "Tue":
        obj.Tuesday = False
        obj.save()
        return
    if day == "Wed":
        obj.Wednesday = False
        obj.save()
        return
    if day == "Thu":
        obj.Thrusday = False
        obj.save()
        return
    if day == "Fri":
        obj.Friday = False
        obj.save()
        return
    if day == "Sat":
        obj.Saturday = False
        obj.save()
        return
    return


def main(Booked,id):

    weekdays = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    shortcut_to_days = {
        "Sun" : "Sunday",
        "Mon" : "Monday",
        "Tue" : "Tuesday",
        "Wed" : "Wednesday",
        "Thu" : "Thrusday",
        "Fri" : "Friday",
        "Sat" : "Saturday",
    }
    Date = []

    today = str(ctime(time())[:3])

    doc_obj = Doctor.objects.get(id=id)
    for i in range(len(weekdays)):
        if weekdays[i] == today:
            split_date = i
            break
        # else:
        #     change(weekdays[i],doc_obj)
        #     Booked[i] = False

    rendering_weekdays = weekdays[split_date:] + weekdays[:split_date]
    rendering_booked = Booked[split_date:] + Booked[:split_date]



    for i in range(7):
        t = float(time()) + float(i*86400)
        Date.append(getDate(t))

    Dict = {}
    for i in range(7):
        Dict[Date[i]] = rendering_booked[i]


    return Dict

