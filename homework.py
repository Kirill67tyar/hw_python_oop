class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        # return (f'Тип тренировки: {self.training_type}; '
        #         f'Длительность: {round(self.duration, 3)} ч.; '
        #         f'Дистанция: {round(self.distance, 3)} км; '
        #         f'Ср. скорость: {round(self.speed, 3)} км/ч; '
        #         f'Потрачено ккал: {round(self.calories, 3)}.')
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

    def __str__(self):
        return self.get_message()


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # длина шага
    M_IN_KM: int = 1000  # 1 км
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,  # кол-во действий
                 duration: float,  # длительность трени
                 weight: float,  # вес
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight
        self.minutes: float = duration * self.MIN_IN_H

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
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
           Формула:
           (18 * средняя_скорость + 1.79)
           * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах
        """
        mean_speed: float = self.get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    IN_MET_S: float = 0.278
    FROM_SM_TO_M: int = 100

    def __init__(self,
                 action: int,  # кол-во действий
                 duration: float,  # длительность трени
                 weight: float,  # вес в кг.
                 height: int,  # рост в см.
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
           Формула:
           ((0.035 * вес +
           (средняя_скорость_в_метрах_в_секунду ** 2 / рост_в_метрах)
           * 0.029 * вес) * время_тренировки_в_минутах)
        """
        mean_sp_met: float = self.get_mean_speed() * self.IN_MET_S
        height_in_m: float = self.height / self.FROM_SM_TO_M
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
                 + (mean_sp_met ** 2 / height_in_m)
                 * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                * self.minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    FOR_CALC_CALORIES_1: float = 1.1
    FOR_CALC_CALORIES_2: int = 2

    def __init__(self,
                 action: int,  # кол-во действий
                 duration: float,  # длительность трени
                 weight: float,  # вес
                 length_pool: int,  # длина бассейна в метрах
                 count_pool: int,  # кол-во переплыл басик
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
           Формула:
           (средняя_скорость + 1.1) * 2 * вес * время_тренировки
        """
        mean_speed = self.get_mean_speed()
        return ((mean_speed + self.FOR_CALC_CALORIES_1)
                * self.FOR_CALC_CALORIES_2 * self.weight * self.duration)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения.
           Формула:
           длина_бассейна * count_pool / M_IN_KM / время_тренировки
        """
        return (self.length_pool * self.count_pool
                / self.M_IN_KM
                / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
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
