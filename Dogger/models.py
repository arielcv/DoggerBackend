from django.contrib.auth.models import AbstractUser, User
from django.db import models
import bisect
import datetime


# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    password = models.CharField(max_length=100)


class DogOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    bio = models.TextField(null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.user.username if self.name == '' else self.name
        super(DogOwner, self).save()

    def __str__(self):
        return str(self.name)


class Dog(models.Model):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = "large"

    CATEGORIES = ((SMALL, 'Small'),
                  (MEDIUM, 'Medium'),
                  (LARGE, 'Large'))

    name = models.CharField(max_length=50, unique=True)
    size = models.CharField(max_length=50, choices=CATEGORIES)
    owner = models.ForeignKey(DogOwner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TimeStamp(models.Model):
    walker = models.ForeignKey('DogWalker', on_delete=models.CASCADE)
    dt = models.DateTimeField(unique=True)
    before = models.IntegerField(default=0)
    after = models.IntegerField(default=0)

    def isBegin(self):
        self.after += 1

    def couldBeBegin(self):
        return True if self.after < 3 else False

    def isEnd(self):
        self.before += 1

    def couldBeEnd(self):
        return True if self.before < 3 else False

    def isMiddle(self):
        self.isBegin()
        self.isEnd()

    def couldBeMiddle(self):
        return True if self.couldBeBegin() and self.couldBeEnd() else False

    class Meta:
        ordering = ['dt']

    def __str__(self):
        return f'{self.dt}-{self.before}-{self.after}'

    def __repr__(self):
        return f'{self.dt}-{self.before}-{self.after}'

    def __gt__(self, other):
        return True if self.dt > other.dt else False

    def __ge__(self, other):
        return True if self.dt >= other.dt else False

    def __lt__(self, other):
        return True if self.dt < other.dt else False

    def __le__(self, other):
        return True if self.dt <= other.dt else False

    def __eq__(self, other):
        return True if self.dt == other.dt else False

    def __hash__(self):
        return super().__hash__()


class DogWalker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    bio = models.TextField(null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.user.username if self.name == '' else self.name
        super(DogWalker, self).save()

    def __str__(self):
        return self.name

    def assign(self, startString, endString):

        lowerList = TimeStamp.objects.filter(dt__lt=startString.dt, walker=self)
        upperList = TimeStamp.objects.filter(dt__gt=endString.dt, walker=self)
        timeStampList = list(TimeStamp.objects.filter(dt__gte=startString.dt, dt__lte=endString.dt, walker=self))
        arrayUpdates = []
        (left, right) = False, False
        if timeStampList:
            if timeStampList[0] == startString:
                if timeStampList[0].couldBeBegin():
                    timeStampList[0].isBegin()
                    arrayUpdates.append(timeStampList[0])
                    left = True
                else:
                    return False
            elif lowerList:
                if lowerList.last().couldBeBegin():
                    startString.before = lowerList.last().after
                    startString.after = startString.before + 1
                    arrayUpdates.append(startString)
            elif lowerList.last() is None:
                startString.before = 0
                startString.after = 1
                arrayUpdates.append(startString)
            else:
                return False
            if timeStampList[-1] == endString:
                if timeStampList[-1].couldBeEnd():
                    endString = timeStampList[-1]
                    endString.isEnd()
                    arrayUpdates.append(endString)
                    right = True
                else:
                    return False
            elif upperList:
                if upperList.first().couldBeEnd():
                    endString.after = upperList.first().before
                    endString.before = endString.after + 1
                    arrayUpdates.append(endString)
            elif upperList.last() is None:
                endString.before = 1
                endString.after = 0
                arrayUpdates.append(endString)
            else:
                return False
            if left:
                timeStampList = timeStampList[1:]
            if right:
                timeStampList = timeStampList[:-1]
            updates = self.updateInterval(timeStampList)
            if updates or updates == []:
                arrayUpdates += updates
                return arrayUpdates
            else:
                return False

        else:
            startString.before = 0
            startString.after = 1
            arrayUpdates.append(startString)
            endString.before = 1
            endString.after = 0
            arrayUpdates.append(endString)
            return arrayUpdates

    def validateSchedule(self, start, end):
        if end <= start:
            print('The ending time is before the starting time or the duration is 0')
            raise KeyError
        return (start, end)

    def updateInterval(self, interval):
        arrayUpdates = []
        for dt in interval:
            if not (dt.couldBeMiddle()):
                return False
            else:
                dt.isMiddle()
                arrayUpdates.append(dt)
        return arrayUpdates


class Reservation(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    walker = models.ForeignKey(DogWalker,on_delete=models.CASCADE)
    owner = models.ForeignKey(DogOwner, on_delete=models.CASCADE)

