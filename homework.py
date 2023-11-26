from dataclasses import (
    asdict,
    dataclass
)


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE_FOR_OUTPUT = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Получить информационное сообщение о тренировке."""
        return self.MESSAGE_FOR_OUTPUT.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int  # кол-во действий
    duration: float  # продолжительность трени в часах
    weight: float  # вес спорстмена
    LEN_STEP = 0.65  # длина шага
    M_IN_KM = 1000  # 1 км
    MIN_IN_HOUR = 60  # минут в часе

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise AttributeError('Method \'get_spent_calories\''
                             'available only in subclasses')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18.0
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        minutes: float = self.duration * self.MIN_IN_HOUR
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * minutes
                )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029
    METERS_IN_SECOND = 0.278
    CENTIMETERS_IN_METER = 100

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        minutes: float = self.duration * self.MIN_IN_HOUR
        mean_speed_met_per_sec: float = (self.get_mean_speed()
                                         * self.METERS_IN_SECOND)
        height_in_m: float = self.height / self.CENTIMETERS_IN_METER
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                 + (mean_speed_met_per_sec ** 2 / height_in_m)
                 * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                * minutes
                )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float  # длина бассейна в метрах
    count_pool: int  # кол-во переплыл басик
    LEN_STEP = 1.38
    FOR_CALC_CALORIES_1 = 1.1
    FOR_CALC_CALORIES_2 = 2.0

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.FOR_CALC_CALORIES_1)
                * self.FOR_CALC_CALORIES_2 * self.weight * self.duration
                )

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM
                / self.duration
                )


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type not in workout_classes:
        available_keys = ', '.join(workout_classes.keys())
        raise KeyError(f'wrong key - \'{workout_type}\'. '
                       f'\'workout_classes\' only accepts keys: '
                       f'{available_keys}')
    return workout_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
