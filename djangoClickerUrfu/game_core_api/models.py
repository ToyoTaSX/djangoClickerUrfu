from django.db import models
from django.contrib.auth.models import User
# Для уровня          2    3    4      5      6      7      8      9      10
POINTS_TO_LEVEL_UP = [100, 500, 10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**9]

class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    points_to_level_up = models.IntegerField(default=POINTS_TO_LEVEL_UP[0])


    def click(self) -> bool:
        self.points += self.click_power
        if self.points >= self.points_to_level_up:
            self.level += 1
            self.points_to_level_up = POINTS_TO_LEVEL_UP[self.level - 1]
            self.save()
            return True
        self.save()
        return False

class Boost(models.Model):
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE)
    price = models.IntegerField(default=10)
    power = models.IntegerField(default=10)
    level = models.IntegerField(default=1)

    def buy(self):
        if self.core.points < self.price:
            return False

        self.core.click_power += self.power
        self.core.points -= self.price
        self.price *= 5
        self.level += 1
        self.core.save()
        self.save()
        return True
