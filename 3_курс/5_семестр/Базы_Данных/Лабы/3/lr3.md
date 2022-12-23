 
1. Выбрать всех подписчиков указанного издания

        CREATE VIEW t_subs_pub_donkey
        AS SELECT fio as Подписчики_на_Мин_говор_ослы
        FROM t_subs
        JOIN t_publishing on idpub=id
        JOIN t_pod on t_subs.idpod=t_pod.id
        WHERE pubname='Миниатюрные говорящие ослы';


2. Для каждого издания подсчитать количество подписчиков.

        CREATE VIEW t_cpod_publishings
        AS SELECT
        pubname AS Издание,
        COUNT(idpod) AS Количество_подписчиков
        FROM t_subs
        JOIN t_publishing ON t_subs.idpub=t_publishing.id
        GROUP BY idpub, pubname;


3. Получить действительный на указанную дату список подписчиков с указанием адресов и изданий, на которые они подписаны.

        CREATE VIEW t_pods_2017_07_21
        AS SELECT fio as ФИО,
        'Регион ' || t_address.region || ', город ' || t_address.city
        || ', улица ' || t_address.street || ', дом ' || t_address.house
        || ', квартира ' || t_address.apartment as Адрес,
        t_publishing.pubname as Издание
        FROM t_subs
        JOIN t_pod ON t_pod.id=idpod
        JOIN t_publishing ON t_publishing.id=idpub
        JOIN t_pubhouse ON t_pubhouse.id=idpubhouse
        JOIN t_address ON t_address.id=t_pod.idaddr
        WHERE '2017-07-21'  >= datestart
        AND '2017-07-21'  <= datestart + make_interval(months => idperiod);


4. Получить группы подписчиков, проживающих на одной улице в указанном городе, и отсортировать их по номерам домов.

        CREATE VIEW t_novogolvill
        AS SELECT street as Улица_города_Новоголвилль, fio as ФИО
        FROM t_subs
        JOIN t_pod ON t_pod.id=t_subs.idpod
        JOIN t_address ON t_address.id=t_pod.idaddr
        WHERE city='Новоголвилль'
        GROUP BY  street, house, fio
        ORDER BY house

