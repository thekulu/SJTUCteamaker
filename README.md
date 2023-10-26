# SJTUCteamaker

# 先创建自己的数据库，然后修改 SJTUCteamaker\SJTUCteamaker\settings.py 里的 DATABASES
# 然后：
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver 9000
# 第一次是会新输入信息的：在SJTUCteamaker\home_interface\views.py修改信息
# 这个views.py里有两个blogs函数，注释掉的是读取数据库的第一个内容，可以换着使用