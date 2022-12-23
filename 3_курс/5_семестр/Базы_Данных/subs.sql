--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6 (Ubuntu 14.6-1.pgdg22.10+1)
-- Dumped by pg_dump version 15.1 (Ubuntu 15.1-1.pgdg22.10+1)

-- Started on 2022-12-19 20:15:42 +07

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 210 (class 1259 OID 16568)
-- Name: t_address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.t_address (
    id integer NOT NULL,
    post_code character varying(6),
    region character varying(30) NOT NULL,
    city character varying(30) NOT NULL,
    street character varying(50) NOT NULL,
    house integer,
    apartment integer,
    CONSTRAINT t_address_apartment_check CHECK (((apartment > 0) OR NULL::boolean)),
    CONSTRAINT t_address_house_check CHECK ((house > 0))
);


ALTER TABLE public.t_address OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16567)
-- Name: t_address_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.t_address_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.t_address_id_seq OWNER TO postgres;

--
-- TOC entry 3440 (class 0 OID 0)
-- Dependencies: 209
-- Name: t_address_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.t_address_id_seq OWNED BY public.t_address.id;


--
-- TOC entry 214 (class 1259 OID 24872)
-- Name: t_publishing; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.t_publishing (
    id character varying(6) NOT NULL,
    idpubhouse character varying(7),
    pubname character varying(50) NOT NULL,
    description text
);


ALTER TABLE public.t_publishing OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 24898)
-- Name: t_subs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.t_subs (
    idpod integer NOT NULL,
    datestart date NOT NULL,
    idpub character varying(6) NOT NULL,
    idperiod integer NOT NULL
);


ALTER TABLE public.t_subs OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 24995)
-- Name: t_cpod_publishings; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.t_cpod_publishings AS
 SELECT t_publishing.pubname AS "Издание",
    count(t_subs.idpod) AS "Количество_подписчиков"
   FROM (public.t_subs
     JOIN public.t_publishing ON (((t_subs.idpub)::text = (t_publishing.id)::text)))
  GROUP BY t_subs.idpub, t_publishing.pubname;


ALTER TABLE public.t_cpod_publishings OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16577)
-- Name: t_pod; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.t_pod (
    id integer NOT NULL,
    fio character varying(85) NOT NULL,
    idaddr integer
);


ALTER TABLE public.t_pod OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 25004)
-- Name: t_novogolvill; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.t_novogolvill AS
 SELECT t_address.street AS "Улица_города_Новоголвилль",
    t_pod.fio AS "ФИО"
   FROM ((public.t_subs
     JOIN public.t_pod ON ((t_pod.id = t_subs.idpod)))
     JOIN public.t_address ON ((t_address.id = t_pod.idaddr)))
  WHERE ((t_address.city)::text = 'Новоголвилль'::text)
  GROUP BY t_address.street, t_address.house, t_pod.fio
  ORDER BY t_address.house;


ALTER TABLE public.t_novogolvill OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 24887)
-- Name: t_period; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.t_period (
    idpub character varying(6) NOT NULL,
    period integer NOT NULL,
    periodname character varying(20) NOT NULL,
    price money,
    CONSTRAINT period CHECK ((period > 0))
);


ALTER TABLE public.t_period OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16576)
-- Name: t_pod_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.t_pod_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.t_pod_id_seq OWNER TO postgres;

--
-- TOC entry 3441 (class 0 OID 0)
-- Dependencies: 211
-- Name: t_pod_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.t_pod_id_seq OWNED BY public.t_pod.id;


--
-- TOC entry 219 (class 1259 OID 24999)
-- Name: t_pods_2017_07_21; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.t_pods_2017_07_21 AS
 SELECT t_pod.fio AS "ФИО",
    ((((((((('Регион '::text || (t_address.region)::text) || ', город '::text) || (t_address.city)::text) || ', улица '::text) || (t_address.street)::text) || ', дом '::text) || t_address.house) || ', квартира '::text) || t_address.apartment) AS "Адрес",
    t_publishing.pubname AS "Издание"
   FROM (((public.t_subs
     JOIN public.t_pod ON ((t_pod.id = t_subs.idpod)))
     JOIN public.t_publishing ON (((t_publishing.id)::text = (t_subs.idpub)::text)))
     JOIN public.t_address ON ((t_address.id = t_pod.idaddr)))
  WHERE (('2017-07-21'::date >= t_subs.datestart) AND ('2017-07-21 00:00:00'::timestamp without time zone <= (t_subs.datestart + make_interval(months => t_subs.idperiod))));


ALTER TABLE public.t_pods_2017_07_21 OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16617)
-- Name: t_pubhouse; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.t_pubhouse (
    id character varying(7) NOT NULL,
    name character varying(50) NOT NULL,
    idaddr integer,
    phone character varying(15),
    CONSTRAINT t_pubhouse_id_check CHECK (((id)::text ~ similar_to_escape('\d{2,7}'::text))),
    CONSTRAINT t_pubhouse_phone_check CHECK (((phone)::text ~ similar_to_escape('\(\d{4}\) \d{2}-\d{2}-\d{2}'::text)))
);


ALTER TABLE public.t_pubhouse OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24991)
-- Name: t_subs_pub_donkey; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.t_subs_pub_donkey AS
 SELECT t_pod.fio AS "Подписчики_на_Мин_говор_ослы"
   FROM ((public.t_subs
     JOIN public.t_publishing ON (((t_subs.idpub)::text = (t_publishing.id)::text)))
     JOIN public.t_pod ON ((t_subs.idpod = t_pod.id)))
  WHERE ((t_publishing.pubname)::text = 'Миниатюрные говорящие ослы'::text);


ALTER TABLE public.t_subs_pub_donkey OWNER TO postgres;

--
-- TOC entry 3257 (class 2604 OID 16571)
-- Name: t_address id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_address ALTER COLUMN id SET DEFAULT nextval('public.t_address_id_seq'::regclass);


--
-- TOC entry 3258 (class 2604 OID 16580)
-- Name: t_pod id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_pod ALTER COLUMN id SET DEFAULT nextval('public.t_pod_id_seq'::regclass);


--
-- TOC entry 3427 (class 0 OID 16568)
-- Dependencies: 210
-- Data for Name: t_address; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (1, '847275', 'Пивной край', 'Воблинск', 'Трезвых', 20, 52);
INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (2, '634043', 'Райская долина', 'Мухомуромск', 'Нечистой силы', 74, 438);
INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (4, '029817', 'Досадный регион', 'Новоголвилль', 'Провал Синицина', 404, 137);
INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (5, '105736', 'Томная область', 'Шизариумск', 'Ленивка', 1, 1);
INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (6, '847277', 'Пивной край', 'Воблинск', 'Трезвых', 21, 88);
INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (7, '634045', 'Райская долина', 'Мухомуромск', 'Нечистой силы', 101, 555);
INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (8, '029819', 'Досадный регион', 'Новоголвилль', 'Провал Синицина', 500, 404);
INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (9, '029818', 'Досадный регион', 'Новоголвилль', 'Горшок', 77, 47);
INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (10, '029819', 'Досадный регион', 'Новоголвилль', 'Золотова', 38, 26);
INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (11, '029820', 'Досадный регион', 'Новоголвилль', 'Золотова', 39, 47);
INSERT INTO public.t_address (id, post_code, region, city, street, house, apartment) VALUES (3, '572963', 'Стеклянный округ', 'Скрежетальск', 'Артефактов', 336, 77);


--
-- TOC entry 3432 (class 0 OID 24887)
-- Dependencies: 215
-- Data for Name: t_period; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.t_period (idpub, period, periodname, price) VALUES ('194852', 4, 'Любительский', '200,00 ₽');
INSERT INTO public.t_period (idpub, period, periodname, price) VALUES ('503294', 5, 'Стандартный', '100,00 ₽');
INSERT INTO public.t_period (idpub, period, periodname, price) VALUES ('200200', 3, 'Слесарь', '285,00 ₽');
INSERT INTO public.t_period (idpub, period, periodname, price) VALUES ('000294', 12, 'Следователь', '79,00 ₽');
INSERT INTO public.t_period (idpub, period, periodname, price) VALUES ('829485', 6, 'Стандарт', '923,00 ₽');
INSERT INTO public.t_period (idpub, period, periodname, price) VALUES ('194852', 1, 'Хозяин', '300,00 ₽');
INSERT INTO public.t_period (idpub, period, periodname, price) VALUES ('829485', 2, 'Нигилист', '199,00 ₽');
INSERT INTO public.t_period (idpub, period, periodname, price) VALUES ('829485', 1, 'Отчаянный', '2 300,00 ₽');
INSERT INTO public.t_period (idpub, period, periodname, price) VALUES ('294842', 7, 'Дикий', '999,00 ₽');


--
-- TOC entry 3429 (class 0 OID 16577)
-- Dependencies: 212
-- Data for Name: t_pod; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.t_pod (id, fio, idaddr) VALUES (3, 'Пьяных Татьяна Николаевна', 1);
INSERT INTO public.t_pod (id, fio, idaddr) VALUES (1, 'Камрад Артём Златоустович', 4);
INSERT INTO public.t_pod (id, fio, idaddr) VALUES (5, 'Холявка Елена Васильевна', 5);
INSERT INTO public.t_pod (id, fio, idaddr) VALUES (4, 'Какаев Аркадий Акакиевич', 3);
INSERT INTO public.t_pod (id, fio, idaddr) VALUES (2, 'Добрыйвечер Добромир Миронов', 8);
INSERT INTO public.t_pod (id, fio, idaddr) VALUES (6, 'Фамильяров Геннадий Иннокентьевич', 9);
INSERT INTO public.t_pod (id, fio, idaddr) VALUES (7, 'Шорохова Евгения Олеговна', 10);
INSERT INTO public.t_pod (id, fio, idaddr) VALUES (8, 'Шорохов Олег Евгеньевич', 11);


--
-- TOC entry 3430 (class 0 OID 16617)
-- Dependencies: 213
-- Data for Name: t_pubhouse; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.t_pubhouse (id, name, idaddr, phone) VALUES ('362', 'Кубик огня', 2, '(4870) 53-20-46');
INSERT INTO public.t_pubhouse (id, name, idaddr, phone) VALUES ('2754', 'Изыдий', 3, '(5194) 29-96-68');
INSERT INTO public.t_pubhouse (id, name, idaddr, phone) VALUES ('37', 'Восвоясень', 2, '(4843) 74-26-24');
INSERT INTO public.t_pubhouse (id, name, idaddr, phone) VALUES ('25624', 'Ящер Пандоры', 2, '(4870) 53-20-48');
INSERT INTO public.t_pubhouse (id, name, idaddr, phone) VALUES ('256245', 'Эскимо', 3, '(8850) 11-12-65');
INSERT INTO public.t_pubhouse (id, name, idaddr, phone) VALUES ('93237', 'Пиарфа', 2, '(1520) 98-98-81');
INSERT INTO public.t_pubhouse (id, name, idaddr, phone) VALUES ('9406824', 'Стравинка', 1, '(5162) 32-59-40');


--
-- TOC entry 3431 (class 0 OID 24872)
-- Dependencies: 214
-- Data for Name: t_publishing; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.t_publishing (id, idpubhouse, pubname, description) VALUES ('602948', '93237', 'Девушки и трупы', 'Автор журнала «Девушки и трупы» Роберт Стивен Райн объясняет идею создания подобного издания так: «Ну, если у вас с вами есть что-то общее, то вам нравятся две вещи: красивые девушки и гниющие трупы. И я подумал, почему бы не совместить их в одном журнале?».

Вероятно, что этот журнал — самый странный из всех, что когда-либо издавались. В каждом номере присутствуют фотографии полуобнажённых юных красавиц, позирующих с отвратительными разлагающимися телами. Как говорят редакторы журнала: «Так много трупов… и так мало времени».');
INSERT INTO public.t_publishing (id, idpubhouse, pubname, description) VALUES ('194852', '256245', 'Миниатюрные говорящие ослы', 'Этот журнал посвящён обсуждению ослов всех размеров и выходит вот уже в течение 18-ти лет. В основном в журнале публикуются статьи, содержащие невероятно полезные знания о миниатюрных осликах: как за ними ухаживать, как их купать или чем их кормить. Правда, несмотря на название, ни в одном из номеров нет информации о настоящем говорящем осле, как можно было надеяться, исходя из названия.');
INSERT INTO public.t_publishing (id, idpubhouse, pubname, description) VALUES ('829485', '9406824', 'Современный Пьяница', 'Журнал «Современный Пьяница» выступает за неотъемлемое право каждого человека напиться. Каждый месяц в журнале публикуется информация о новых видах алкоголя и культуре употребления алкогольных напитков.

Создатель журнала Фрэнк Келли Рич заявляет, что общественность относится к любителям выпить несправедливо, делая таких людей «самым притесняемым меньшинством общества». Изначально Рич писал все статьи для своего журнала сам, а в качестве источника информации использовал бездомных алкоголиков. Он просил их дать читателям интересный и неизбитый совет о том, как нужно пить тот или иной алкогольный напиток. За каждый нетривиальный совет он платил 20 долларов. А чтобы журнал выглядел достовернее, Рич наполнял страницы первых выпусков поддельной рекламой.

Типичные заголовки статей «Современного пьяницы» — «Известные атлеты-алкоголики» или «Нажраться одному как форма медитации». А сам главред, по словам его знакомых, действительно придерживается того образа жизни, о котором пишет.');
INSERT INTO public.t_publishing (id, idpubhouse, pubname, description) VALUES ('294842', '25624', 'Медвежья жизнь', 'Если вам нравятся весёлые, мускулистые и волосатые парни, тогда можете почитать этот журнал. В первую очередь журнал посвящён сообществу гомосексуалистов, объединённых одной субкультурой — они называют себя «медведями». Статьи в журнале попадаются весьма специфические. Например, зимой 2007-го года «Медвежья жизнь» опубликовала статью под названием «101 игра: заставьте вашу игру продолжаться!», являющуюся чем-то вроде руководства по играм для таких вот «медведей».');
INSERT INTO public.t_publishing (id, idpubhouse, pubname, description) VALUES ('503294', '37', 'Новости трубочиста', 'Журнал призван пролить свет на то, кто же такие трубочисты на самом деле. Он содержит множество статей непосредственно о профессии трубочиста, их внешнем облике, смешные истории о трубочистах, а также о том, как вести себя, если трубочист пытается содрать с вас лишние деньги. В одном из номеров была статья, смысл которой можно передать так: «прогоняйте любого трубочиста, использующего по отношению к вам тактику запугивания». К сожалению, чтό это за тактика, в статье не уточняется.');
INSERT INTO public.t_publishing (id, idpubhouse, pubname, description) VALUES ('200200', '93237', 'Журнал операторов портативных туалетов', 'Журнал посвящён в первую очередь тому, где следует и где, наоборот, не следует справлять свои естественные потребности, а также людям, которые устанавливают и обслуживают портативные уличные туалеты. В журнале публикуется много фотографий непосредственно туалетных кабинок с описанием их дизайна и функционала. Кроме того, множество ассенизаторов делятся на страницах журнала секретами своей профессии и забавными историями из жизни.');
INSERT INTO public.t_publishing (id, idpubhouse, pubname, description) VALUES ('105927', '256245', 'T-Post', 'Этот журнал необычен тем, что печатается не на бумаге, а на футболках. Слоган издания гласит: «T-Post — это первый журнал, который можно носить на себе». Обложка размещена на передней стороне футболки, а статьи — на спине и изнаночной стороне. Материалы публикуются самые разные: о событиях в мире моды, социальных проблемах, политике, медицине. Часто на «обложках» появляются знаменитости — художники, киноактёры, дизайнеры. Аудитория за девять лет публикаций накопилась огромная, и популярность журнала продолжает расти.');
INSERT INTO public.t_publishing (id, idpubhouse, pubname, description) VALUES ('002395', '25624', 'Лимон', 'Оригинальность журнала заключается в его запахе, не имеющем ничего общего с запахом типографской краски или, как модно в некоторых женских журналах, парфюмом. Между страниц со статьями о модной одежде вставлены ароматизированные страницы с запахом лимона, апельсина или других цитрусовых. Ещё одно приятное отличие издания от других подобных журналов в том, что все статьи в нём связаны между собой: редакция совместно придумывает сюжет для каждого номера, и в результате получается нечто вроде детективной истории с фотографиями современной модной одежды в стиле 1960–1970-х годов с лёгким уклоном в «ретро». Почему именно аромат лимона? — спросите вы. Создатели журнала заявляют, что с таким ароматизатором у читателя непременно возникнет желание дочитать до конца даже самую скучную статью.');
INSERT INTO public.t_publishing (id, idpubhouse, pubname, description) VALUES ('000294', '2754', 'Разыскивается', 'Журнал выходит с периодичностью раз в год. Он посвящён любым вещам, которые потерялись за год: предметы одежды, любовные письма, билеты, стихи на оставленных в кафе салфетках, потерявшие свою пару носки. Материал для журнала поставляют сами читатели: они просто отправляют в редакцию потерянные кем-то другим вещи, найденные ими на улице или в общественных местах. Если вы вдруг обнаружите на страницах журнала принадлежащую вам вещь, то можете написать в редакцию письмо с просьбой её вернуть.');


--
-- TOC entry 3433 (class 0 OID 24898)
-- Dependencies: 216
-- Data for Name: t_subs; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (2, '2019-01-29', '194852', 4);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (1, '2007-07-07', '194852', 1);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (3, '2013-05-02', '194852', 1);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (2, '2018-07-05', '829485', 6);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (5, '2016-08-28', '829485', 1);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (2, '2017-04-23', '000294', 12);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (3, '2009-11-26', '503294', 5);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (1, '2022-10-09', '829485', 6);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (1, '2008-06-15', '294842', 7);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (5, '2005-06-03', '294842', 7);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (6, '2017-05-29', '294842', 7);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (7, '2017-01-03', '000294', 12);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (8, '2017-03-29', '829485', 6);
INSERT INTO public.t_subs (idpod, datestart, idpub, idperiod) VALUES (4, '2017-04-01', '194852', 4);


--
-- TOC entry 3442 (class 0 OID 0)
-- Dependencies: 209
-- Name: t_address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.t_address_id_seq', 4, true);


--
-- TOC entry 3443 (class 0 OID 0)
-- Dependencies: 211
-- Name: t_pod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.t_pod_id_seq', 2, true);


--
-- TOC entry 3263 (class 2606 OID 24944)
-- Name: t_publishing id; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public.t_publishing
    ADD CONSTRAINT id CHECK ((((id)::text ~ similar_to_escape('\d{6}'::text)) AND (NOT ((id)::text = '000000'::text)))) NOT VALID;


--
-- TOC entry 3266 (class 2606 OID 16575)
-- Name: t_address t_address_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_address
    ADD CONSTRAINT t_address_pkey PRIMARY KEY (id);


--
-- TOC entry 3274 (class 2606 OID 24892)
-- Name: t_period t_period_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_period
    ADD CONSTRAINT t_period_pkey PRIMARY KEY (idpub, period);


--
-- TOC entry 3268 (class 2606 OID 16582)
-- Name: t_pod t_pod_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_pod
    ADD CONSTRAINT t_pod_pkey PRIMARY KEY (id);


--
-- TOC entry 3270 (class 2606 OID 24920)
-- Name: t_pubhouse t_pubhouse_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_pubhouse
    ADD CONSTRAINT t_pubhouse_pkey PRIMARY KEY (id);


--
-- TOC entry 3272 (class 2606 OID 24886)
-- Name: t_publishing t_publishing_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_publishing
    ADD CONSTRAINT t_publishing_pkey PRIMARY KEY (id);


--
-- TOC entry 3276 (class 2606 OID 24902)
-- Name: t_subs t_subs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_subs
    ADD CONSTRAINT t_subs_pkey PRIMARY KEY (idpod, idpub, idperiod);


--
-- TOC entry 3281 (class 2606 OID 24903)
-- Name: t_subs idpod; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_subs
    ADD CONSTRAINT idpod FOREIGN KEY (idpod) REFERENCES public.t_pod(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3280 (class 2606 OID 24893)
-- Name: t_period idpub; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_period
    ADD CONSTRAINT idpub FOREIGN KEY (idpub) REFERENCES public.t_publishing(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3279 (class 2606 OID 24922)
-- Name: t_publishing idpubhouse; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_publishing
    ADD CONSTRAINT idpubhouse FOREIGN KEY (idpubhouse) REFERENCES public.t_pubhouse(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3278 (class 2606 OID 24913)
-- Name: t_pubhouse inaddr; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_pubhouse
    ADD CONSTRAINT inaddr FOREIGN KEY (idaddr) REFERENCES public.t_address(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3282 (class 2606 OID 24945)
-- Name: t_subs period; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_subs
    ADD CONSTRAINT period FOREIGN KEY (idperiod, idpub) REFERENCES public.t_period(period, idpub) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 3277 (class 2606 OID 16583)
-- Name: t_pod t_pod_idaddr_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.t_pod
    ADD CONSTRAINT t_pod_idaddr_fkey FOREIGN KEY (idaddr) REFERENCES public.t_address(id);


--
-- TOC entry 3439 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2022-12-19 20:15:42 +07

--
-- PostgreSQL database dump complete
--

