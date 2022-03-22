from dataclasses import dataclass, fields
from typing import Sequence


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    PHRASE = (
        'Тип тренировки: {0}; '
        'Длительность: {1:.3f} ч.; '
        'Дистанция: {2:.3f} км; '
        'Ср. скорость: {3:.3f} км/ч; '
        'Потрачено ккал: {4:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.PHRASE.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    MIN_IN_H = 60
    LEN_STEP = .65
    RUN_SPEED_MUL = 18
    RUN_SPEED_ADD = 20

    action: str
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.RUN_SPEED_MUL * self.get_mean_speed()
            - self.RUN_SPEED_ADD)
            * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_H
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    pass


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    S_WALK_WEIGHT_MUL = .035
    S_WALK_SPEED_MUL = .029

    height: float

    def get_spent_calories(self) -> float:
        return (
            (self.S_WALK_WEIGHT_MUL * self.weight
            + self.get_mean_speed() ** 2 // self.height
            * self.S_WALK_SPEED_MUL * self.weight)
            * self.duration * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWIM_SPEED_ADD = 1.1
    SWIM_CALORIES_MUL = 2
    
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SWIM_SPEED_ADD)
            * self.SWIM_CALORIES_MUL * self.weight
        )

def read_package(workout_type: str, data: Sequence[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    sought_class = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }[workout_type]
    return sought_class(*data[:len(fields(sought_class))])

def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
