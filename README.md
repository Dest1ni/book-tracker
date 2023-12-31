# Сервис «Библиотека» - автоматизация учета выдачи книг читателям.
Это тестовое задание со следующей формулировкой:

Цель: создать сервис «Библиотека» - автоматизация учета выдачи книг читателям.

Функционал:
1)	Создание книг – книги имеют название и автора. У одного автора может быть несколько книг (Выполнено)
2)	Учет читателей – читатель имеет Фамилию, Имя и Отчество. Один читатель может быть зарегистрирован в библиотеке один раз. Читатель может взять одновременно несколько книг (Выполнено)
3)	Учет выдачи книг – фиксация даты, когда была выдана книга читателю и когда она была возвращена читателем (Выполнено)
4)	Учет хранения книг – по запросу возможность определить какие книги есть на остатках в библиотеке, какие книги выданы читателям (Выполнено)

Описание работы:
Читатель входит в систему, выбирая свою Фамилию из списка. Если читателя нет в списке, он может добавить свои данные в систему. Далее читатель использую сервис, может выбрать одно из двух действий: посмотреть список доступных книг или сдать книгу. При выборе первого пункта, читатель, получает список книг с кодами. Он может взять книгу используя код книги, либо завершить работу с системой. При выборе «сдать книгу» читатель указывает код взятой книги, и система возвращает ее на остатки. Действия по взятию книг и возврату книг фиксируются в системе.

Технологии:
Хранение данных: База данных MySQL, SQLite на выбор
Языки программирования (на выбор): Python, JavaScript (возможно использовать фреймворки), PHP, C#, Java,Golang, 1С
Управление системой: команды консоли, либо web-интерфейс. Использование web интерфейса будет плюсом.

Результат: 
Исходные коды приложения с описанием технологического стека
Краткое описание работы с системой
Выгрузка базы данных, с указанием используемой БД
