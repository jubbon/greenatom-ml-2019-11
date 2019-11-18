#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main():
    ''' Обучает модель
    '''

    try:
        print(f"Начинается обучение модели", flush=True)
        # TODO: вместо импорта перенести сюда часть кода из app.py
        import app
        print(f"Обучение модели завершено", flush=True)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
