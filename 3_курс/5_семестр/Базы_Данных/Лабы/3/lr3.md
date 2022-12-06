 
1. Выбрать всех подписчиков указанного издания

        SELECT fio
        FROM t_subs JOIN t_publishing on idpub=id
                    JOIN t_pod on t_subs.idpod=t_pod.id
        WHERE pubname='Миниатюрные говорящие ослы'


2. Для каждого издания подсчитать количество подписчиков.

        SELECT idpub, COUNT(idpod)
        FROM t_subs
        GROUP BY idpub


        SELECT COUNT(idpod), pubname
        FROM t_subs JOIN t_publishing ON t_subs.idpub=t_publishing.id
        GROUP BY idpub, pubname


3. Получить действительный на указанную дату список подписчиков с указанием адресов и изданий, на которые они подписаны.

        SELECT fio, t_address.region, t_publishing.pubname
        FROM t_subs JOIN t_pod ON idpod=t_pod.id
                    JOIN t_publishing ON idpub=t_publishing.id
                    JOIN t_pubhouse ON idpubhouse=t_pubhouse.id
                    JOIN t_address ON t_pubhouse.idaddr=t_address.id
        WHERE datestart>'2013-01-01'


4. Получить группы подписчиков, проживающих на одной улице в указанном городе, и отсортировать их по номерам домов.
