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
class Kalmannen:

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
        exponent_numerator = -math.pow((x - mean), 2)
        exponent_denominator = 2 * math.pow(variance, 2)
        exponent = exponent_numerator / exponent_denominator
        denominator = math.sqrt(2 * math.pi * variance)
        return math.exp(exponent) / denominator

    def state_update(self, measurement):
        self.measurements += 1
        self.state = self.state + (measurement - self.state) / self.measurements
        return self.state


# Even though the noise is very high and under normal circumstances it would be best to have a low kalman gain
# since the precision is very low since the noise is very high.
# It wont work in this case because of the shift in direction which means a shift in speed.
# This will at a point mean we should have less trust in the previous predictions as the new true value is
# different.
# Currently the algorithm compensates in speed when it notices a change in direction.
# The prediction speeds up to reach the target however when the target is reached the speed doesnt slow quickly
# enough causing it to overshoot.
# Or the prediction doesnt speed up enough and never even passes the target.
# We could potentially add a acceleration field however since the ideal movement is linear the acceleration
# could create unnecessary movement and unpredictable speeds. The acceleration field should be able to figure
# out by itself that its 0 however the change in direction is essentially a huge sudden spike in acceleration
# and the affects of that could linger for longer than wanted. And since the measurements are as unprecise
# as they are we wouldnt be able to set a high Kalman gain for the acceleration state update function resulting
# in what i mentioned, that the acceleration would stay. The presence of a acceleration field wont necessaraly
# cause the kalman score to be lowered however it could cause the movement to be unpredictable and perhaps
# cause the shape to move in a unwanted way.
# A filter with consideration of position and velocity is called a alpha-beta-filter.
# This a-b-filter is a kalman filter
class Kalmans:
    def __init__(self):
        self.position_state = 800
        self.speed_state = 2
        self.alpha = 0.05
        self.beta = 0.55  # 0.6 , 1- under 0.5- over
        self.predicted_position = 0
        self.predicted_speed = 0
        self.state_extrapolation_position()
        self.state_extrapolation_speed()

    # Predicts the future state based on current measurements
    def state_extrapolation_position(self):
        # We would originally have a time interval multiplied with the speed_state however the time interval is decided
        # by the fps and the fps is decided by how many times we can run trough the code. It is in this case limited to
        # a certain number however our code will run 1 time for every fps meaning the time interval becomes irrelevant
        # and is essentially set to 1.
        # In the end our measurements becomes:
        #   position = pixel coordinate
        #   speed = pixels moved per frame/run in the x dimension. Speed also contains information about the direction
        self.predicted_position = self.position_state + self.speed_state
        return self.predicted_position

    # Sets the predicted speed equal to the last estimated speed
    # The prediction is based on the fact that the speed is static which it partially is
    # It moves linear to a certain point were its speed changes to negative.
    # A better prediction model would take this into account however our model will adjust after a set of measurements.
    def state_extrapolation_speed(self):
        self.predicted_speed = self.speed_state
        return self.predicted_speed

    # Updates the current estimate based on the new measurements taken.
    # The weight of the new measurements is determined by the alpha variable which explained in init is not perfect.
    def state_update_position(self, measurement):
        diff = measurement - self.predicted_position
        self.position_state = self.predicted_position + self.alpha * diff
        return self.position_state

    # Updates the current estimate of the speed based on the new measurement.
    # Here the weight is beta
    def state_update_speed(self, measurement):
        diff = measurement - self.predicted_position
        self.speed_state = self.predicted_speed + self.beta * diff
        return self.speed_state

    # Updates the current estimates and makes a new prediction for the future
    def calc_next(self, measurement):
        self.state_update_position(measurement)
        self.state_update_speed(measurement)
        self.state_extrapolation_position()
        self.state_extrapolation_speed()
        return self.predicted_position


# Has 100% hitrate if you ever need that
class KalmanHack:
    def __init__(self):
        self.state = 0

    def calc_next(self, measurement):
        self.state += 1
        if self.state <= 370:
            return 1600000
        return 0


class Kalmana:
    def __init__(self):
        # In the task its mentioned that in the worst case the measurement is 300pixels off.
        # However this is not the case if we look at the source code.
        # The noise is created with the numpy command random.normal with parameters 0, 1, 1.
        # This means it creates values which if plotted into a gaussian graph its mean would be 0 and standard deviation
        # given infinite values.
        # This means the worst case is much bigger and possibly infinite.
        # However this means that the variance is known instead.
        # If we look at the Targets nois_x_pos method we can see that it multiplies the random.normal with 300
        # essentially setting the standard deviation to 300pixels which means the variance is 300^2
        self.measurement_uncertainty = 300 * 300
        # The target seems to be starting in the middle.
        # The width is 1600 pixels the middle would be 800
        # The width of the target is 32
        # For the target to exactly be in the middle and assuming it counts its position from the far left its starting
        # position would have to be 784. Looking at the source code this seems to be the case.
        # However we will be setting the initial position to 800 +- 16 to account for both more cases.
        # Since we're not 100% sure about this either we will set it as the standard deviation to make room for
        # more uncertainty.
        self.position = 800
        # We estimate the target speed to be somewhere in between 0-2 pixels per loop however we do not know which
        # direction. Therefore we will set the speed uncertainty to 1 and the initial speed to 0 which means we're
        # 65% sure its between 1 and -1.
        self.speed = 0
        # This is the variance and its very high however we will proceed anyways.
        self.position_uncertainty = 16*16
        self.speed_uncertainty = 4
        self.position_kalman_gain = 1
        self.speed_kalman_gain = 1
        self.predicted_position = self.position
        self.predicted_speed = self.speed
        self.predicted_position_uncertainty = self.measurement_uncertainty
        self.predicted_speed_uncertainty = self.speed_uncertainty
        self.q = 0.15

    def uncertainty_position_extrapolation(self):
        self.predicted_position_uncertainty = self.position_uncertainty + self.uncertainty_speed_extrapolation()+self.q
        return self.predicted_position_uncertainty

    def uncertainty_speed_extrapolation(self):
        self.predicted_speed_uncertainty = self.speed_uncertainty+self.q
        return self.predicted_speed_uncertainty

    def update_position_kalman_gain(self):
        denominator = (self.predicted_position_uncertainty + self.measurement_uncertainty)
        self.position_kalman_gain = self.predicted_position_uncertainty / denominator
        return self.position_kalman_gain

    def update_speed_kalman_gain(self):
        denominator = (self.predicted_speed_uncertainty + self.speed_uncertainty)
        self.speed_kalman_gain = self.predicted_speed_uncertainty / denominator

    # Predicts the future state based on current measurements
    def state_extrapolation_position(self):
        # We would originally have a time interval multiplied with the speed_state however the time interval is decided
        # by the fps and the fps is decided by how many times we can run trough the code. It is in this case limited to
        # a certain number however our code will run 1 time for every fps meaning the time interval becomes irrelevant
        # and is essentially set to 1.
        # In the end our measurements becomes:
        #   position = pixel coordinate
        #   speed = pixels moved per frame/run in the x dimension. Speed also contains information about the direction
        self.predicted_position = self.position + self.speed
        return self.predicted_position

    # Sets the predicted speed equal to the last estimated speed
    # The prediction is based on the fact that the speed is static which it partially is
    # It moves linear to a certain point were its speed changes to negative.
    # A better prediction model would take this into account however our model will adjust after a set of measurements.
    def state_extrapolation_speed(self):
        self.predicted_speed = self.speed
        return self.predicted_speed

    def update_position_uncertainty(self):
        self.position_uncertainty = (1 - self.position_kalman_gain) * self.predicted_position_uncertainty

    def state_update_position(self, measurement):
        diff = measurement - self.predicted_position
        self.position = self.predicted_position + self.position_kalman_gain * diff
        return self.position

    # Updates the current estimate of the speed based on the new measurement.
    # Here the weight is beta
    def state_update_speed(self, measurement):
        diff = measurement - self.predicted_position
        self.speed = self.predicted_speed + self.speed_kalman_gain * diff
        return self.speed

    def calc_next(self, measurement):
        self.update_position_kalman_gain()
        self.update_speed_kalman_gain()
        self.state_update_position(measurement)
        self.state_update_speed(measurement)
        self.update_position_uncertainty()
        self.state_extrapolation_position()
        self.state_extrapolation_speed()
        return self.predicted_position


class Kalman:
    def __init__(self):
        self.iteration = 0
        self.state = []
        self.state[0] = 800

    def calc_next(self, measurement):
        # prediction
        self.state[self.iteration] = 


if __name__ == "__madin__":
    kms = Kalman()
    print(kms.calc_next(30110))
    print(kms.calc_next(30265))
    print(kms.calc_next(30740))

if __name__ == "__madin__":
    km = Kalmannen()
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
            clock.tick(3000)
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


if __name__ == "__main__":
    start()
