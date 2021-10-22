# coding=utf8
'''
#
# Obligatorisk karaktersatt oppgave #1
#
# Legg spesielt merke til at det er kun koden i klassen Kalman som kan endres. Det er koden som skal leveres inn
# Det er derfor viktig at INGEN ANNEN KODE ENDRES !!! 
#
'''
import math

import pygame as pg
from random import random, randint
import numpy as np
from numpy.linalg import norm
import pytest

fps = 0.0


class Projectile():

    def __init__(self, background, kalman=None):
        self.background = background
        self.rect = pg.Rect((800, 700), (16, 16))
        self.px = self.rect.x
        self.py = self.rect.y
        self.dx = 0.0
        self.kalm = kalman

    def move(self, goal):

        if self.kalm:
            goal = self.kalm.calc_next(goal)

        deltax = np.array(float(goal) - self.px)
        # print(delta2)
        mag_delta = norm(deltax)  # * 500.0
        np.divide(deltax, mag_delta, deltax)

        self.dx += deltax
        # if self.dx:
        # self.dx /= norm(self.dx) * 50

        self.px += self.dx / 50.0
        self.py += -0.5
        try:
            self.rect.x = int(self.px)
        except:
            pass
        try:
            self.rect.y = int(self.py)
        except:
            pass


class Target():

    def __init__(self, background, width):
        self.background = background
        self.rect = pg.Rect(self.background.get_width() // 2 - width // 2,
                            50, width, 32)
        self.dx = 1 if random() > 0.5 else -1

    def move(self):
        self.rect.x += self.dx

        if self.rect.x < 300 or self.rect.x > self.background.get_width() - 300:
            self.dx *= -1

    def noisy_x_pos(self):
        pos = self.rect.x
        center = self.rect.width // 2
        noise = np.random.normal(0, 1, 1)[0]

        return pos + center + noise * 300.0


#
# Her er Kalmanfilteret du skal utvikle
#
# The following
class Kalman:

    def __init__(self):
        # Inital guess.
        self.state = 1000
        self.measurements = 0

    def calc_next(self, zi):
        return 800
        pass

    # Calculates the average value of a list of numbers
    # List must contain either int or float objects
    # Returns a floating number which may result in microscopic inaccuracies
    def calc_mean(self, values: list) -> float:
        result = 0
        for x in values:
            if isinstance(x, float) or isinstance(x, int):
                result += x
            else:
                raise Exception("Non float or int object detected in list")
        return result / len(values)

    # Calculates the variance
    # The variance is:
    #   the sum of:
    #       value minus the mean of the value
    #           squared
    #   Divided by the number of values
    def calc_variance(self, values: list) -> float:
        mean = self.calc_mean(values)
        result = 0
        for x in values:
            # math.pow squares the result of x - mean
            # math.pow always returns a floating number
            # x is a value from the list
            result += math.pow((x - mean), 2)
        return result / len(values)

    def calc_standard_deviation(self, values: list) -> float:
        variance = self.calc_variance(values)
        return math.sqrt(variance)

    # When the variance is being estimated we have to account that the mean is also being estimated
    # Using the estimated mean to calculate the variance will always result in a smaller variance than if we used
    # the true mean. Unless the estimated mean is exactly the same as the true mean, which by that point it wont be an
    # estimation.
    # To compensate for this we use the normalizing factor n - 1 instead of just n.
    # The n represents the number of values in the list calculated by len(list).
    # Else it uses the same methods as "calc_variance".
    def estimate_variance(self, values: list) -> float:
        mean = self.calc_mean(values)
        result = 0
        for x in values:
            # math.pow squares the result of x - mean
            # x is a value from the list
            result += math.pow((x - mean), 2)
        normalizing_factor = len(values) - 1
        return result / normalizing_factor

    # Will create the normal distribution if plotted by x
    # Also has other potential such as plotting by mean and variance.
    def probability_density(self, x, mean, variance) -> float:
        exponent_numerator = -math.pow((x-mean), 2)
        exponent_denominator = 2*math.pow(variance, 2)
        exponent = exponent_numerator / exponent_denominator
        denominator = math.sqrt(2*math.pi*variance)
        return math.exp(exponent) / denominator

    def state_update(self, measurement):
        self.measurements += 1
        self.state = self.state + (measurement-self.state)/self.measurements
        return self.state



if __name__ == "__main__":
    km = Kalman()
    lst = [1.89, 2.1, 1.75, 1.98, 1.85]
    lstb = [1.94, 1.9, 1.97, 1.89, 1.87]
    r = km.calc_standard_deviation(lst)
    r2 = km.calc_standard_deviation(lstb)
    print(km.state)
    print(km.state_update(1030))
    print(km.state)
    print(km.state_update(989))
    print(km.state)
    print(km.state_update(1017))
    print(km.state)



def start():
    pg.init()

    w, h = 1600, 800

    background = pg.display.set_mode((w, h))
    surf = pg.surfarray.pixels3d(background)
    running = True
    clock = pg.time.Clock()

    kalman_score = 0
    reg_score = 0
    iters = 0

    while running:
        target = Target(background, 32)
        missile = Projectile(background)
        k_miss = Projectile(background, Kalman())  # kommenter inn denne linjen naar Kalman er implementert
        last_x_pos = target.noisy_x_pos
        noisy_draw = np.zeros((w, 20))

        trial = True
        iters += 1

        while trial:

            # Setter en maksimal framerate på 300. Hvis dere vil øke denne er dette en mulig endring
            clock.tick(100)
            fps = clock.get_fps()

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    running = False

            background.fill(0x448844)
            surf[:, 0:20, 0] = noisy_draw

            last_x_pos = target.noisy_x_pos()
            # print(last_x_pos)

            target.move()
            missile.move(last_x_pos)
            k_miss.move(last_x_pos)  # kommenter inn denne linjen naar Kalman er implementert

            pg.draw.rect(background, (255, 200, 0), missile.rect)
            pg.draw.rect(background, (0, 200, 255),
                         k_miss.rect)  # kommenter inn denne linjen naar Kalman er implementert
            pg.draw.rect(background, (255, 200, 255), target.rect)

            noisy_draw[int(last_x_pos):int(last_x_pos) + 20, :] = 255
            noisy_draw -= 1
            np.clip(noisy_draw, 0, 255, noisy_draw)

            coll = missile.rect.colliderect(target.rect)
            k_coll = k_miss.rect.colliderect(target.rect)  # kommenter inn denne linjen naar Kalman er implementert#

            if coll:
                reg_score += 1

            if k_coll:  # kommenter inn denne linjen naar Kalman er implementert
                kalman_score += 1

            oob = missile.rect.y < 20

            if oob or coll or k_coll:  # endre denne sjekken slik at k_coll ogsaa er med naar kalman er implementert
                trial = False

            pg.display.flip()

        print('kalman score: ',
              round(kalman_score / iters, 2))  # kommenter inn denne linjen naar Kalman er implementert
        print('regular score: ', round(reg_score / iters, 2))

    pg.quit()

# if __name__ == "__main__":
# start()
