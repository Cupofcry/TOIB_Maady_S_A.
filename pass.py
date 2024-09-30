import hashlib
import requests

def check_password_pwned(password):
    # Используем SHA-1 для хэширования пароля
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1_password[:5], sha1_password[5:]

    # Отправляем первые 5 символов хеша на pwned passwords
    url = f"https://api.pwnedpasswords.com/range/{first5}"
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError(f'Ошибка при обращении к API: {response.status_code}')

    # Получаем список возможных совпадений
    hashes = (line.split(':') for line in response.text.splitlines())

    # Проверяем, есть ли полное совпадение хеша
    for h, count in hashes:
        if h == tail:
            return f"Пароль найден в базе утечек {count} раз(а)."

    return "Пароль не найден в базе утечек."

if __name__ == "__main__":
    password = input("Введите пароль для проверки в базе утечек: ")
    result = check_password_pwned(password)
    print(result)