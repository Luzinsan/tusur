sudo -i -u postgres
psql





    \dt - выводит имя_отношения

    \d имя_таблицы - отображение таблицы

    \l - выводит все базы данных

    q - выйти из режима просмотра

CREATE DATABASE имя_базы_данных
\c имя_базы_данных

CREATE TABLE имя_отношения

## Типы данных столбцов:
- varchar(N)
- char(N) - дополняет строку пробелами
- serial - автоматическое заполнение значений (счётчик)
- timestamp - время и дата
- text - неограниченная строка

## Ограничения
### ПК
- первичный ключ - уникальное поле, предотвращающее дублируемость (позволяет идентифицировать отдельную сущность)
для указания первичного ключа используется ограничение PRIMARY KEY
Пример:
id serial PRIMARY KEY

### NULL\NOT NULL
- (не)ограничивает допустимость пустого поля

### UNIQUE
- помечается уникальное поле


Внешний ключ (связывает разные таблицы между собой) - поддерживает целостность
### REFERENCES имя_таблицы(поле)
- типы полей должны совпадать

Пример:
| ПК
| NOT NULL
| NOT NULL + UNIQUE

Реализация:
CREATE TABLE students(
id serial PRIMARY KEY,
name varchar(20) NOT NULL,
passport int NOT NULL UNIQUE);

## Логические ограничения полей
- CHECK(логическое_выражение)
Пример:
age int CHECK(age>=18 and age<=81)

## Ограничения всей таблицы
PRIMARY KEY(поле1, поле2, ...) - присваивает ПК нескольким столбцам
FOREIGN KEY(поле1, поле2, ...) REFERENCES имя_связанной_таблицы (внеш_поле1, внеш_поле2, ...)

Пример:

    CREATE TABLE students(
    id int PRIMARY KEY,
    name varchar(20) NOT NULL,
    passport int NOT NULL UNIQUE);


    CREATE TABLE test2(
    id int,
    external_id int REFERENCES students(id),
    age int CHECK(age>=18 and age<=81),
    PRIMARY KEY(id, external_id));

test_db=# \d students

                        Table "public.students"
    Column  |         Type          | Collation | Nullable | Default
    ----------+-----------------------+-----------+----------+---------
    id       | integer               |           | not null |
    name     | character varying(20) |           | not null |
    passport | integer               |           | not null |

    Indexes:
        "students_pkey" PRIMARY KEY, btree (id)
        "students_passport_key" UNIQUE CONSTRAINT, btree (passport)
    Referenced by:
        TABLE "test2" CONSTRAINT "test2_external_id_fkey" FOREIGN KEY (external_id) REFERENCES students(id)

test_db=# \d test2

                    Table "public.test2"
    Column    |  Type   | Collation | Nullable | Default
    -------------+---------+-----------+----------+---------
    id          | integer |           | not null |
    external_id | integer |           | not null |
    age         | integer |           |          |
    Indexes:
        "test2_pkey" PRIMARY KEY, btree (id, external_id)
    Check constraints:
        "test2_age_check" CHECK (age >= 18 AND age <= 81)
    Foreign-key constraints:
        "test2_external_id_fkey" FOREIGN KEY (external_id) REFERENCES students(id)


INSERT INTO students(id, name, passport) VALUES (43030, 'Vanya', 102947), (43035, 'Gennadiy', 384295);


SELECT *
FROM students
WHERE name='Vanya'
;


UPDATE students
SET name='Vasiliy'
WHERE id=43030 AND passport=102947;

- если не указывать условие WHERE, то значение обновится во всех строках поля

DELETE
FROM test2
WHERE id=43029;

ALTER TABLE students
ADD average_mark integer CHECK(average_mark<=5 and average_mark>=0),
DROP COLUMN passport;

ALTER TABLE user_list
ADD CONSTRAINT name CHECK(name SIMILAR TO '[а-яА-ЯёЁ]');

test_db=# DELETE
FROM user_list
WHERE id=3;
DELETE 1
test_db=# ALTER TABLE user_list                                                             DROP CONSTRAINT name;
ALTER TABLE
test_db=# ALTER TABLE user_list                                                             ADD CONSTRAINT name CHECK(name SIMILAR TO '[а-яА-ЯёЁ ]*');
ALTER TABLE
test_db=# INSERT INTO user_list(name, email, age) VALUES ('Анастасия Лузинсан', 'luzinsan@mail.ru', 19);
INSERT 0 1
test_db=# SELECT *                                                                          FROM user_list;
 id |        name        |      email       | age
----+--------------------+------------------+-----
  4 | Анастасия Лузинсан | luzinsan@mail.ru |  19
(1 row)







