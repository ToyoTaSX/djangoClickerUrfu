from django.db import models
from django.contrib.auth.models import User
# Для уровня          2    3    4      5      6      7      8      9      10
POINTS_TO_LEVEL_UP = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]

class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    click_power = models.IntegerField(default=5)
    level = models.IntegerField(default=1)
    points_to_level_up = models.IntegerField(default=POINTS_TO_LEVEL_UP[0])
    frame = models.IntegerField(default=0)
    frame_url = models.TextField(default=f"/static/img/click_images/frame0.png")


    def click(self) -> bool:
        self.points += self.click_power
        self.frame = (self.frame + 1) % 20
        self.frame_url = f"/static/img/click_images/frame{self.frame}.png"
        if self.points >= self.points_to_level_up and self.level <= 12:
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
    img_rel_url = models.URLField(default="None")
    name = models.TextField(default="None")
    names = ['Кефир',
             'Чифир',
             'Балтика 0',
             'Балтика 1',
             'Балтика 2',
             'Балтика 3',
             'Балтика 5',
             'Балтика 7',
             'Балтика 8',
             'Балтика 9',
             'Водка',
             'Самогон деда']

    def __init__(self, *args, **kwargs):
        super(Boost, self).__init__(*args, **kwargs)
        # Установка значения нового поля на основе других полей
        if self.img_rel_url == "None":
            self.img_rel_url = f"/static/img/boost_images/{self.core.level - 1}.png"
        if self.name == "None":
            self.name = self.names[self.core.level - 2]

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
