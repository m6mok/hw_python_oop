from dataclasses import dataclass, fields, asdict
from typing import Sequence


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    PHRASE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.PHRASE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    MIN_IN_H = 60
    LEN_STEP = .65

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
        pass

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
    SPEED_MULTIPLIER = 18
    SPEED_ADDITIVE = -20

    def get_spent_calories(self) -> float:
        return ((
            self.SPEED_MULTIPLIER * self.get_mean_speed()
            + self.SPEED_ADDITIVE)
            * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER = .035
    SPEED_MULTIPLIER = .029

    height: float

    def get_spent_calories(self) -> float:
        return ((
            self.WEIGHT_MULTIPLIER * self.weight
            + self.get_mean_speed() ** 2 // self.height
            * self.SPEED_MULTIPLIER * self.weight)
            * self.duration * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SPEED_ADDITIVE = 1.1
    CALORIES_MULTIPLIER = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SPEED_ADDITIVE)
            * self.CALORIES_MULTIPLIER * self.weight
        )


CLASSES = {
    'RUN': {
        'class': Running,
        'fields_count': len(fields(Running))
    },
    'WLK': {
        'class': SportsWalking,
        'fields_count': len(fields(SportsWalking))
    },
    'SWM': {
        'class': Swimming,
        'fields_count': len(fields(Swimming))
    }
}
STRING_VALUE_ERROR_TEXT = 'Некорректное значение аттрибута: "{value}".'
SEQUENCE_VALUE_ERROR_TEXT = (
    'Количество элементов аргумента '
    'не совпадает с количестом полей класса {class_name}.\n'
    'Требуется: {required}. Найдено: {found}.'
)


def read_package(workout_type: str, data: Sequence[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in CLASSES:
        raise ValueError(
            STRING_VALUE_ERROR_TEXT.format(value=workout_type)
        )
    if len(data) != CLASSES[workout_type]['fields_count']:
        raise ValueError(
            SEQUENCE_VALUE_ERROR_TEXT.format(
                class_name=CLASSES[workout_type]['class'].__name__,
                required=CLASSES[workout_type]['fields_count'],
                found=len(data)
            )
        )
    return CLASSES[workout_type]['class'](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
