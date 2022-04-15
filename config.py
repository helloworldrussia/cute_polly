from environs import Env


# создадим переменные на основе данных от env для импорта их из разных частей кода
env = Env()
env.read_env()

SECRET = env.str('secret')
EHOST = env.str('ehost')
EPORT = env.int('eport')
EUSER = env.str('ehost_user')
EPASSWORD = env.str('ehost_password')