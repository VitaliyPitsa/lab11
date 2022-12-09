#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import datetime
import json


def get_train():
    punkt_nazn = input("Пункт назначения ")
    nomer = input("Номер поезда? ")
    time_str = input("время отправления? (hh/mm)\n ")
    time = datetime.datetime.strptime(time_str, '%H/%M').time()
    return {
        'punkt_nazn': punkt_nazn,
        'nomer': nomer,
        'time': time,
    }


def display_trains(trains):
    if trains:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "No",
                "Пункт назначиния",
                "Номер поезда",
                "время отправления"
            )
        )
        print(line)
        for idx, train in enumerate(trains, 1):
            time = train.get('time', '')
            print(
                '| {:>4} | {:<30} | {:<20} | {}{} |'.format(
                    idx,
                    train.get('punkt_nazn', ''),
                    train.get('nomer', ''),
                    time,
                    ' ' * 5
                )
            )
        print(line)


def select_train(trains, nomer):
    result = [train for train in trains if train.get('nomer', '') == nomer]
    return result


def save_train(file_name, staff):
    """
    Сохранить все рейсы в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4, default=str)


def load_train(file_name):
    """
    Загрузить все поезда из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main():
    global train
    trains = []
    while True:
        command = input(">>> ").lower()
        if command == 'exit':
            break
        elif command == 'add':
            train = get_train()
            trains.append(train)
            if len(trains) > 1:
                trains.sort(key=lambda item: item.get('nomer')[::-1])
        elif command == 'list':
            display_trains(trains)
        elif command.startswith('select'):
            print("Введите номер поезда: ")
            nom = input()
            selected = select_train(trains, nom)
            display_trains(selected)
        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить поезд;")
            print("list - вывести список поездов;")
            print("select найти информацию о поезде по номеру")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")
        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_train(file_name, trains)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            train = load_train(file_name)
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
