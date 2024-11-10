import enum


class GenderEnum(str, enum.Enum):
    MALE = "мужчина"
    FEMALE = "женщина"


class ProfessionEnum(str, enum.Enum):
    DEVELOPER = "разработчик"
    DESIGNER = "дизайнер"
    MANAGER = "менеджер"
    TEACHER = "учитель"
    DOCTOR = "врач"
    ENGINEER = "инженер"
    MARKETER = "маркетолог"
    WRITER = "писатель"
    ARTIST = "художник"
    LAWYER = "юрист"
    SCIENTIST = "ученый"
    NURSE = "медсестра"
    UNEMPLOYED = "безработный"


class RoleEnum(str, enum.Enum):
    ADMIN = "администратор"
    MODERATOR = "модератор"
    USER = "пользователь"


class DiagnosesEnum(str, enum.Enum):
    DIABETES = "диабет"
    HYPERTENSION = "гипертония"
    ASTHMA = "астма"
    DEPRESSION = "депрессия"
    ANXIETY = "тревожное расстройство"
    ARTHRITIS = "артрит"
    HEART_DISEASE = "сердечно-сосудистые заболевания"
    CANCER = "рак"
    ALLERGY = "аллергия"
    INFECTION = "инфекция"
    OBESITY = "ожирение"
    MIGRAINE = "мигрень"
    HEALTHY = "здоров"
