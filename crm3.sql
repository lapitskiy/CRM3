-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 11 2022 г., 15:24
-- Версия сервера: 10.3.22-MariaDB
-- Версия PHP: 7.1.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `crm3`
--

-- --------------------------------------------------------

--
-- Структура таблицы `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(33, 'Can add log entry', 1, 'add_logentry'),
(34, 'Can change log entry', 1, 'change_logentry'),
(35, 'Can delete log entry', 1, 'delete_logentry'),
(36, 'Can view log entry', 1, 'view_logentry'),
(37, 'Can add permission', 2, 'add_permission'),
(38, 'Can change permission', 2, 'change_permission'),
(39, 'Can delete permission', 2, 'delete_permission'),
(40, 'Can view permission', 2, 'view_permission'),
(41, 'Can add group', 3, 'add_group'),
(42, 'Can change group', 3, 'change_group'),
(43, 'Can delete group', 3, 'delete_group'),
(44, 'Can view group', 3, 'view_group'),
(45, 'Can add user', 4, 'add_user'),
(46, 'Can change user', 4, 'change_user'),
(47, 'Can delete user', 4, 'delete_user'),
(48, 'Can view user', 4, 'view_user'),
(49, 'Can add content type', 5, 'add_contenttype'),
(50, 'Can change content type', 5, 'change_contenttype'),
(51, 'Can delete content type', 5, 'delete_contenttype'),
(52, 'Can view content type', 5, 'view_contenttype'),
(53, 'Can add session', 6, 'add_session'),
(54, 'Can change session', 6, 'change_session'),
(55, 'Can delete session', 6, 'delete_session'),
(56, 'Can view session', 6, 'view_session'),
(57, 'Can add Новость', 7, 'add_news'),
(58, 'Can change Новость', 7, 'change_news'),
(59, 'Can delete Новость', 7, 'delete_news'),
(60, 'Can view Новость', 7, 'view_news'),
(61, 'Can add Категория', 8, 'add_category'),
(62, 'Can change Категория', 8, 'change_category'),
(63, 'Can delete Категория', 8, 'delete_category'),
(64, 'Can view Категория', 8, 'view_category'),
(65, 'Can add Плагин', 11, 'add_plugins'),
(66, 'Can change Плагин', 11, 'change_plugins'),
(67, 'Can delete Плагин', 11, 'delete_plugins'),
(68, 'Can view Плагин', 11, 'view_plugins'),
(69, 'Can add Категория', 9, 'add_pluginscategory'),
(70, 'Can change Категория', 9, 'change_pluginscategory'),
(71, 'Can delete Категория', 9, 'delete_pluginscategory'),
(72, 'Can view Категория', 9, 'view_pluginscategory'),
(73, 'Can add Категория', 18, 'add_category'),
(74, 'Can change Категория', 18, 'change_category'),
(75, 'Can delete Категория', 18, 'delete_category'),
(76, 'Can view Категория', 18, 'view_category'),
(77, 'Can add Устройство', 24, 'add_device'),
(78, 'Can change Устройство', 24, 'change_device'),
(79, 'Can delete Устройство', 24, 'delete_device'),
(80, 'Can view Устройство', 24, 'view_device'),
(81, 'Can add Услуга', 16, 'add_service'),
(82, 'Can change Услуга', 16, 'change_service'),
(83, 'Can delete Услуга', 16, 'delete_service'),
(84, 'Can view Услуга', 16, 'view_service'),
(85, 'Can add Статус', 15, 'add_status'),
(86, 'Can change Статус', 15, 'change_status'),
(87, 'Can delete Статус', 15, 'delete_status'),
(88, 'Can view Статус', 15, 'view_status'),
(89, 'Can add Заказ', 14, 'add_orders'),
(90, 'Can change Заказ', 14, 'change_orders'),
(91, 'Can delete Заказ', 14, 'delete_orders'),
(92, 'Can view Заказ', 14, 'view_orders'),
(93, 'Can add Клиент', 20, 'add_clients'),
(94, 'Can change Клиент', 20, 'change_clients'),
(95, 'Can delete Клиент', 20, 'delete_clients'),
(96, 'Can view Клиент', 20, 'view_clients'),
(97, 'Can add Деньги', 23, 'add_money'),
(98, 'Can change Деньги', 23, 'change_money'),
(99, 'Can delete Деньги', 23, 'delete_money'),
(100, 'Can view Деньги', 23, 'view_money'),
(101, 'Can add Форма', 25, 'add_prints'),
(102, 'Can change Форма', 25, 'change_prints'),
(103, 'Can delete Форма', 25, 'delete_prints'),
(104, 'Can view Форма', 25, 'view_prints'),
(105, 'Can add Категория', 26, 'add_category'),
(106, 'Can change Категория', 26, 'change_category'),
(107, 'Can delete Категория', 26, 'delete_category'),
(108, 'Can view Категория', 26, 'view_category'),
(109, 'Can add Отделения', 27, 'add_storehouses'),
(110, 'Can change Отделения', 27, 'change_storehouses'),
(111, 'Can delete Отделения', 27, 'delete_storehouses'),
(112, 'Can view Отделения', 27, 'view_storehouses'),
(113, 'Can add Связанные отделения', 28, 'add_storerelated'),
(114, 'Can change Связанные отделения', 28, 'change_storerelated'),
(115, 'Can delete Связанные отделения', 28, 'delete_storerelated'),
(116, 'Can view Связанные отделения', 28, 'view_storerelated');

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Дамп данных таблицы `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(2, 'pbkdf2_sha256$216000$1ZxOy3mNVDuW$crghWULGbbD7BQg7KbllMAkQg0Y7d3QdsPrH7SKlQ7c=', '2022-04-11 11:49:40.420102', 1, 'lapitsky', '', '', 'lapithome@gmail.com', 1, 1, '2022-04-11 11:49:27.132342');

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `auth_user_user_permissions`
--

INSERT INTO `auth_user_user_permissions` (`id`, `user_id`, `permission_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 1, 5),
(6, 1, 6),
(7, 1, 7),
(8, 1, 8),
(9, 1, 9),
(10, 1, 10),
(11, 1, 11),
(12, 1, 12),
(13, 1, 13),
(14, 1, 14),
(15, 1, 15),
(16, 1, 16),
(17, 1, 17),
(18, 1, 18),
(19, 1, 19),
(20, 1, 20),
(21, 1, 21),
(22, 1, 22),
(23, 1, 23),
(24, 1, 24),
(25, 1, 25),
(26, 1, 26),
(27, 1, 27),
(28, 1, 28),
(29, 1, 29),
(30, 1, 30),
(31, 1, 31),
(32, 1, 32),
(33, 1, 33),
(34, 1, 34),
(35, 1, 35),
(36, 1, 36),
(37, 1, 37),
(38, 1, 38),
(39, 1, 39),
(40, 1, 40),
(41, 1, 41),
(42, 1, 42),
(43, 1, 43),
(44, 1, 44),
(45, 1, 53),
(46, 1, 54),
(47, 1, 55),
(48, 1, 56),
(49, 1, 57),
(50, 1, 58),
(51, 1, 59),
(52, 1, 60);

-- --------------------------------------------------------

--
-- Структура таблицы `clients_clients`
--

CREATE TABLE `clients_clients` (
  `id` int(11) NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(17) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `related_uuid` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL
) ;

--
-- Дамп данных таблицы `clients_clients`
--

INSERT INTO `clients_clients` (`id`, `name`, `phone`, `created_at`, `updated_at`, `related_uuid`) VALUES
(28, 'Egor', '+79211234567', '2021-05-08 23:59:52.892664', '2021-05-20 23:05:55.873103', '{\"4M8XnFY8ybMG9ucum6JyFW\": \"\", \"JbAHMMHnwyEVM3cPjRWRcA\": \"\", \"Ex7bjyiyEfnyg7q4oKcAzo\": \"\"}'),
(31, 'eg', '+79216840525', '2021-05-19 21:30:21.466113', '2021-12-26 17:52:44.439093', '{\"EK9ZduAavU7LNLgz5JNwW7\": \"\", \"55EoLaFncaDDkDbFAeJhe2\": \"\", \"PS7LRcCVsf83BKHZZPAeRk\": \"\"}'),
(32, 'Egor', '+79121234567', '2021-05-20 23:04:38.895700', '2021-05-20 23:05:35.021910', '{}'),
(33, 'test', '+79121234566', '2021-07-12 21:59:11.035539', '2021-07-12 21:59:11.035539', '{\"k9vLs7CqZaipigeouUtETZ\": \"\"}'),
(34, 'test', '+79121234563', '2021-07-12 21:59:36.009968', '2022-01-16 22:04:27.536314', '{\"o53hfjYQymdV8DjCe4ANAo\": \"\", \"Dyqg8eT8BjGVp74nJcgmDm\": \"\"}');

-- --------------------------------------------------------

--
-- Структура таблицы `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2021-02-02 22:13:30.545561', '1', 'Культура', 1, '[{\"added\": {}}]', 8, 1),
(2, '2021-02-02 22:13:35.202828', '2', 'Политика', 1, '[{\"added\": {}}]', 8, 1),
(3, '2021-02-04 11:54:28.133732', '1', '123', 1, '[{\"added\": {}}]', 7, 1),
(4, '2021-02-05 11:13:45.062793', '1', 'trst', 1, '[{\"added\": {}}]', 10, 1),
(5, '2021-02-07 12:33:17.290344', '1', '123', 2, '[{\"changed\": {\"fields\": [\"\\u0424\\u043e\\u0442\\u043e\"]}}]', 7, 1),
(6, '2021-02-12 22:07:51.766158', '1', 'lapitsky', 2, '[{\"changed\": {\"fields\": [\"User permissions\"]}}]', 4, 1),
(7, '2021-02-13 23:09:58.614118', '1', 'Test', 1, '[{\"added\": {}}]', 9, 1),
(8, '2021-02-22 19:46:59.016376', '1', 'Заказ', 1, '[{\"added\": {}}]', 16, 1),
(9, '2021-02-22 19:47:59.413830', '2', 'Быстрый заказ', 1, '[{\"added\": {}}]', 16, 1),
(10, '2021-02-22 19:48:08.960376', '3', 'Продажа', 1, '[{\"added\": {}}]', 16, 1),
(11, '2021-02-23 12:12:09.026298', '1', 'Принят', 1, '[{\"added\": {}}]', 15, 1),
(12, '2021-02-23 12:17:18.947025', '2', 'Диагностика', 1, '[{\"added\": {}}]', 15, 1),
(13, '2021-02-23 12:18:39.619639', '3', 'Готов', 1, '[{\"added\": {}}]', 15, 1),
(14, '2021-02-23 12:19:01.910914', '4', 'Отказ', 1, '[{\"added\": {}}]', 15, 1),
(15, '2021-02-23 18:01:18.365532', '1', 'test', 1, '[{\"added\": {}}]', 17, 1),
(16, '2021-02-24 19:29:25.634107', '1', 'fast', 1, '[{\"added\": {}}]', 18, 1),
(17, '2021-02-24 19:29:41.897037', '2', 'Обычный заказ', 1, '[{\"added\": {}}]', 18, 1),
(18, '2021-02-24 19:29:49.324462', '1', 'Быстрый заказ', 2, '[{\"changed\": {\"fields\": [\"\\u041d\\u0430\\u0438\\u043c\\u0435\\u043d\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u043a\\u0430\\u0442\\u0435\\u0433\\u043e\\u0440\\u0438\\u0438\"]}}]', 18, 1),
(19, '2021-03-02 20:25:32.781741', '41', 'Заказы', 2, '[{\"changed\": {\"fields\": [\"\\u0421\\u0432\\u044f\\u0437\\u044c\"]}}]', 11, 1),
(20, '2021-03-02 20:26:50.759201', '3', 'PluginsRelated object (3)', 1, '[{\"added\": {}}]', 22, 1),
(21, '2021-03-04 19:47:12.322060', '41', 'Заказы', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(22, '2021-03-04 19:47:33.498271', '43', 'Клиенты', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(23, '2021-03-04 21:00:27.024423', '43', 'Клиенты', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(24, '2021-03-04 21:00:47.587599', '41', 'Заказы', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(25, '2021-03-12 23:54:29.344719', '41', 'Заказы', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(26, '2021-03-17 12:00:51.390383', '43', 'Клиенты', 2, '[{\"changed\": {\"fields\": [\"\\u0418\\u043c\\u044f \\u043a\\u043b\\u0430\\u0441\\u0441\\u0430 \\u0434\\u043b\\u044f \\u0441\\u0432\\u044f\\u0437\\u0438\"]}}]', 11, 1),
(27, '2021-03-25 22:45:58.621454', '44', 'Бухгалтерия', 2, '[{\"changed\": {\"fields\": [\"\\u0418\\u043c\\u044f \\u043a\\u043b\\u0430\\u0441\\u0441\\u0430 \\u0434\\u043b\\u044f \\u0441\\u0432\\u044f\\u0437\\u0438\"]}}]', 11, 1),
(28, '2021-03-29 23:36:17.273306', '19', 'zcxzcxzc', 3, '', 14, 1),
(29, '2021-03-29 23:36:17.334309', '18', 'zcxzcxzc', 3, '', 14, 1),
(30, '2021-03-29 23:36:17.363311', '17', 'zcxzcxzc', 3, '', 14, 1),
(31, '2021-03-29 23:36:17.391313', '16', 'zcxzcxzc', 3, '', 14, 1),
(32, '2021-03-29 23:36:17.421314', '15', 'xxxxx', 3, '', 14, 1),
(33, '2021-03-29 23:36:17.451316', '14', 'zcxzcxzc', 3, '', 14, 1),
(34, '2021-03-30 15:42:25.841575', '1', 'Заказы в ремонт', 2, '[{\"changed\": {\"fields\": [\"\\u041d\\u0430\\u0438\\u043c\\u0435\\u043d\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u043a\\u0430\\u0442\\u0435\\u0433\\u043e\\u0440\\u0438\\u0438\", \"\\u041a\\u0430\\u0442\\u0435\\u0433\\u043e\\u0440\\u0438\\u044f\"]}}]', 18, 1),
(35, '2021-03-30 15:42:34.612077', '1', 'Быстрые заказы', 2, '[{\"changed\": {\"fields\": [\"\\u041d\\u0430\\u0438\\u043c\\u0435\\u043d\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u043a\\u0430\\u0442\\u0435\\u0433\\u043e\\u0440\\u0438\\u0438\"]}}]', 18, 1),
(36, '2021-03-30 15:42:49.077904', '2', 'Заказы в ремонт', 2, '[{\"changed\": {\"fields\": [\"\\u041d\\u0430\\u0438\\u043c\\u0435\\u043d\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u043a\\u0430\\u0442\\u0435\\u0433\\u043e\\u0440\\u0438\\u0438\", \"\\u041a\\u0430\\u0442\\u0435\\u0433\\u043e\\u0440\\u0438\\u044f\"]}}]', 18, 1),
(37, '2021-03-30 15:47:33.456170', '1', 'Заказ на месте', 2, '[{\"changed\": {\"fields\": [\"\\u041d\\u0430\\u0438\\u043c\\u0435\\u043d\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u043a\\u0430\\u0442\\u0435\\u0433\\u043e\\u0440\\u0438\\u0438\"]}}]', 18, 1),
(38, '2021-03-30 15:47:43.524745', '2', 'Заказ в ремонт', 2, '[{\"changed\": {\"fields\": [\"\\u041d\\u0430\\u0438\\u043c\\u0435\\u043d\\u043e\\u0432\\u0430\\u043d\\u0438\\u044f \\u043a\\u0430\\u0442\\u0435\\u0433\\u043e\\u0440\\u0438\\u0438\"]}}]', 18, 1),
(39, '2021-04-02 00:04:13.728456', '20', 'ewrwerewr', 2, '[{\"changed\": {\"fields\": [\"\\u041a\\u0430\\u0442\\u0435\\u0433\\u043e\\u0440\\u0438\\u044f\"]}}]', 14, 1),
(40, '2021-04-20 23:04:13.434137', '1', 'Замена батареек', 1, '[{\"added\": {}}]', 16, 1),
(41, '2021-04-20 23:04:22.438652', '2', 'Замена стекла', 1, '[{\"added\": {}}]', 16, 1),
(42, '2021-05-04 13:09:29.681110', '6', 'Casio', 1, '[{\"added\": {}}]', 14, 1),
(43, '2021-05-04 13:10:58.164171', '1', '1', 3, '', 14, 1),
(44, '2021-05-06 22:29:39.496038', '24', '+79626840525', 3, '', 20, 1),
(45, '2021-05-06 22:30:33.489126', '25', '', 3, '', 20, 1),
(46, '2021-05-06 22:30:33.551129', '22', '', 3, '', 20, 1),
(47, '2021-05-06 22:30:33.579131', '21', '', 3, '', 20, 1),
(48, '2021-05-06 22:30:33.609133', '20', '', 3, '', 20, 1),
(49, '2021-05-06 22:30:33.639134', '19', '', 3, '', 20, 1),
(50, '2021-05-06 22:30:33.668136', '18', '', 3, '', 20, 1),
(51, '2021-05-06 22:30:33.698138', '17', '', 3, '', 20, 1),
(52, '2021-05-06 22:30:33.728140', '16', '', 3, '', 20, 1),
(53, '2021-05-06 22:30:33.758141', '15', '', 3, '', 20, 1),
(54, '2021-05-06 22:30:33.789143', '14', '+7343434111', 3, '', 20, 1),
(55, '2021-05-06 22:30:33.819145', '13', '+723232323', 3, '', 20, 1),
(56, '2021-05-06 22:30:33.851147', '12', '+723213213', 3, '', 20, 1),
(57, '2021-05-06 22:30:33.884148', '11', '+7213232323', 3, '', 20, 1),
(58, '2021-05-06 22:30:33.918150', '10', '+71231232131', 3, '', 20, 1),
(59, '2021-05-06 22:30:33.952152', '9', '+7121212121221', 3, '', 20, 1),
(60, '2021-05-06 22:30:33.983154', '8', '+71111111111111', 3, '', 20, 1),
(61, '2021-05-06 22:30:34.012156', '7', '+766666666666', 3, '', 20, 1),
(62, '2021-05-06 22:30:34.041157', '6', '+722222222222', 3, '', 20, 1),
(63, '2021-05-06 22:30:34.069159', '5', '+444444444444', 3, '', 20, 1),
(64, '2021-05-06 22:30:34.099161', '4', '+7111111111111', 3, '', 20, 1),
(65, '2021-05-06 22:30:34.127162', '3', '+79213213213213', 3, '', 20, 1),
(66, '2021-05-06 22:30:34.156164', '2', '+7123123213213', 3, '', 20, 1),
(67, '2021-05-06 22:30:34.188166', '1', '+711111111111111', 3, '', 20, 1),
(68, '2021-05-08 22:44:20.595431', '15', 'выавыа', 3, '', 14, 1),
(69, '2021-05-08 23:04:36.180959', '12', '12', 2, '[{\"changed\": {\"fields\": [\"\\u0421\\u0442\\u0430\\u0442\\u0443\\u0441\"]}}]', 14, 1),
(70, '2021-05-08 23:04:47.906629', '14', '14', 3, '', 14, 1),
(71, '2021-05-08 23:04:47.935631', '12', '12', 3, '', 14, 1),
(72, '2021-05-08 23:04:47.965633', '11', '11', 3, '', 14, 1),
(73, '2021-05-08 23:04:47.993634', '9', '9', 3, '', 14, 1),
(74, '2021-05-08 23:04:48.023636', '8', '8', 3, '', 14, 1),
(75, '2021-05-08 23:04:48.051637', '7', '7', 3, '', 14, 1),
(76, '2021-05-08 23:04:48.081639', '6', '6', 3, '', 14, 1),
(77, '2021-05-08 23:06:00.885803', '27', '', 3, '', 20, 1),
(78, '2021-05-08 23:06:00.916805', '26', '+79216840526', 3, '', 20, 1),
(79, '2021-05-08 23:06:00.945807', '23', '+79216840525', 3, '', 20, 1),
(80, '2021-05-08 23:26:28.469017', '22', '0.00', 3, '', 23, 1),
(81, '2021-05-08 23:26:28.538021', '21', '0.00', 3, '', 23, 1),
(82, '2021-05-08 23:26:28.572023', '20', '0.00', 3, '', 23, 1),
(83, '2021-05-08 23:26:28.606025', '19', '123213.00', 3, '', 23, 1),
(84, '2021-05-08 23:26:28.640027', '18', '100.00', 3, '', 23, 1),
(85, '2021-05-08 23:26:28.673029', '17', '0.00', 3, '', 23, 1),
(86, '2021-05-08 23:26:28.719031', '16', '0.00', 3, '', 23, 1),
(87, '2021-05-08 23:26:28.765034', '15', '0.00', 3, '', 23, 1),
(88, '2021-05-08 23:26:28.806036', '14', '0.00', 3, '', 23, 1),
(89, '2021-05-08 23:26:28.847039', '13', '0.00', 3, '', 23, 1),
(90, '2021-05-08 23:26:28.887041', '12', '6667.00', 3, '', 23, 1),
(91, '2021-05-08 23:26:28.927043', '11', '0.00', 3, '', 23, 1),
(92, '2021-05-08 23:26:28.960045', '10', '0.00', 3, '', 23, 1),
(93, '2021-05-08 23:26:28.995047', '9', '0.00', 3, '', 23, 1),
(94, '2021-05-08 23:26:29.026049', '8', '0.00', 3, '', 23, 1),
(95, '2021-05-08 23:26:29.056051', '7', '13213.00', 3, '', 23, 1),
(96, '2021-05-08 23:26:29.089053', '6', '123.00', 3, '', 23, 1),
(97, '2021-05-08 23:26:29.119054', '5', '123.00', 3, '', 23, 1),
(98, '2021-05-08 23:26:29.149056', '4', '123.00', 3, '', 23, 1),
(99, '2021-05-08 23:26:29.180058', '3', '4444.00', 3, '', 23, 1),
(100, '2021-05-08 23:26:29.217060', '2', '111103.00', 3, '', 23, 1),
(101, '2021-05-08 23:26:29.258062', '1', '1200.00', 3, '', 23, 1),
(102, '2021-05-17 22:52:57.583728', '29', '+79211234567', 3, '', 20, 1),
(103, '2021-05-18 22:19:19.053447', '28', '123213.00', 3, '', 23, 1),
(104, '2021-05-19 00:06:09.669114', '30', '+79216840525', 3, '', 20, 1),
(105, '2021-06-14 18:04:53.203448', '7', 'Appella', 2, '[{\"changed\": {\"fields\": [\"Used\"]}}]', 24, 1),
(106, '2021-06-14 18:04:57.249679', '3', 'Casio', 2, '[{\"changed\": {\"fields\": [\"Used\"]}}]', 24, 1),
(107, '2021-06-14 18:05:01.472921', '5', 'Casio Edifice', 2, '[{\"changed\": {\"fields\": [\"Used\"]}}]', 24, 1),
(108, '2021-06-14 18:05:05.406146', '6', 'Casio G-Shock', 2, '[{\"changed\": {\"fields\": [\"Used\"]}}]', 24, 1),
(109, '2021-06-14 18:05:09.595385', '9', 'Tissot', 2, '[{\"changed\": {\"fields\": [\"Used\"]}}]', 24, 1),
(110, '2021-07-13 22:52:58.490219', '16', '16', 2, '[{\"changed\": {\"fields\": [\"\\u0421\\u0442\\u0430\\u0442\\u0443\\u0441\"]}}]', 14, 1),
(111, '2021-07-23 22:28:23.495727', '48', 'Печать', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(112, '2021-07-23 22:32:25.213553', '41', 'Заказы', 2, '[{\"changed\": {\"fields\": [\"\\u0418\\u043c\\u044f \\u043a\\u043b\\u0430\\u0441\\u0441\\u0430 \\u0434\\u043b\\u044f \\u0441\\u0432\\u044f\\u0437\\u0438\"]}}]', 11, 1),
(113, '2021-07-27 22:52:54.090024', '41', 'Заказы', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(114, '2021-07-27 23:01:02.303948', '48', 'Печать', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(115, '2021-07-27 23:03:47.153377', '44', 'Бухгалтерия', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(116, '2021-07-27 23:04:06.634491', '41', 'Заказы', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(117, '2021-07-27 23:05:51.259475', '41', 'Заказы', 2, '[{\"changed\": {\"fields\": [\"Related\"]}}]', 11, 1),
(118, '2021-07-27 23:18:03.445354', '48', 'Печать', 2, '[{\"changed\": {\"fields\": [\"\\u0418\\u043c\\u044f \\u043a\\u043b\\u0430\\u0441\\u0441\\u0430 \\u0434\\u043b\\u044f \\u0441\\u0432\\u044f\\u0437\\u0438\"]}}]', 11, 1),
(119, '2021-10-05 22:32:56.602901', '3', 'test2', 2, '[{\"changed\": {\"fields\": [\"User permissions\"]}}]', 4, 1),
(120, '2021-10-05 22:35:46.747633', '3', 'test2', 2, '[{\"changed\": {\"fields\": [\"Staff status\"]}}]', 4, 1),
(121, '2021-10-05 22:36:54.950534', '3', 'test2', 2, '[{\"changed\": {\"fields\": [\"User permissions\"]}}]', 4, 1),
(122, '2021-10-05 23:27:38.653624', '3', 'test2', 2, '[{\"changed\": {\"fields\": [\"User permissions\"]}}]', 4, 1),
(123, '2021-10-06 23:52:09.026267', '3', 'test2', 2, '[{\"changed\": {\"fields\": [\"User permissions\"]}}]', 4, 1),
(124, '2021-12-27 15:32:49.030275', '49', 'Отделения', 2, '[{\"changed\": {\"fields\": [\"\\u0418\\u043c\\u044f \\u043a\\u043b\\u0430\\u0441\\u0441\\u0430 \\u0434\\u043b\\u044f \\u0441\\u0432\\u044f\\u0437\\u0438\"]}}]', 11, 1),
(125, '2022-01-08 11:15:47.549496', '49', 'Отделения', 2, '[{\"changed\": {\"fields\": [\"\\u0418\\u043c\\u044f \\u043a\\u043b\\u0430\\u0441\\u0441\\u0430 \\u0434\\u043b\\u044f \\u0441\\u0432\\u044f\\u0437\\u0438\"]}}]', 11, 1),
(126, '2022-01-16 20:18:01.855074', '1', '1', 1, '[{\"added\": {}}]', 28, 1),
(127, '2022-01-16 20:18:40.437281', '1', '1', 2, '[{\"changed\": {\"fields\": [\"Related uuid\"]}}]', 28, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(20, 'clients', 'clients'),
(19, 'clients', 'related'),
(5, 'contenttypes', 'contenttype'),
(23, 'money', 'money'),
(8, 'news', 'category'),
(7, 'news', 'news'),
(18, 'orders', 'category'),
(24, 'orders', 'device'),
(14, 'orders', 'orders'),
(17, 'orders', 'related'),
(16, 'orders', 'service'),
(15, 'orders', 'status'),
(11, 'plugins', 'plugins'),
(9, 'plugins', 'pluginscategory'),
(10, 'plugins', 'pluginscrm3'),
(22, 'plugins', 'pluginsrelated'),
(21, 'plugins', 'related'),
(25, 'prints', 'prints'),
(6, 'sessions', 'session'),
(26, 'storehouse', 'category'),
(27, 'storehouse', 'storehouses'),
(28, 'storehouse', 'storerelated');

-- --------------------------------------------------------

--
-- Структура таблицы `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2021-02-02 22:10:26.290023'),
(2, 'auth', '0001_initial', '2021-02-02 22:10:26.361027'),
(3, 'admin', '0001_initial', '2021-02-02 22:10:26.475033'),
(4, 'admin', '0002_logentry_remove_auto_add', '2021-02-02 22:10:26.511035'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2021-02-02 22:10:26.519036'),
(6, 'contenttypes', '0002_remove_content_type_name', '2021-02-02 22:10:26.553038'),
(7, 'auth', '0002_alter_permission_name_max_length', '2021-02-02 22:10:26.574039'),
(8, 'auth', '0003_alter_user_email_max_length', '2021-02-02 22:10:26.589040'),
(9, 'auth', '0004_alter_user_username_opts', '2021-02-02 22:10:26.599040'),
(10, 'auth', '0005_alter_user_last_login_null', '2021-02-02 22:10:26.615041'),
(11, 'auth', '0006_require_contenttypes_0002', '2021-02-02 22:10:26.617041'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2021-02-02 22:10:26.626042'),
(13, 'auth', '0008_alter_user_username_max_length', '2021-02-02 22:10:26.648043'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2021-02-02 22:10:26.669044'),
(15, 'auth', '0010_alter_group_name_max_length', '2021-02-02 22:10:26.680045'),
(16, 'auth', '0011_update_proxy_permissions', '2021-02-02 22:10:26.689045'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2021-02-02 22:10:26.709046'),
(18, 'news', '0001_initial', '2021-02-02 22:10:26.718047'),
(19, 'news', '0002_auto_20210120_0124', '2021-02-02 22:10:26.732048'),
(20, 'news', '0003_auto_20210123_0142', '2021-02-02 22:10:26.754049'),
(21, 'news', '0004_auto_20210201_0201', '2021-02-02 22:10:26.793051'),
(22, 'sessions', '0001_initial', '2021-02-02 22:10:26.801052'),
(23, 'news', '0005_auto_20210204_1354', '2021-02-04 10:55:04.601909'),
(27, 'plugins', '0001_initial', '2021-02-06 22:46:22.313529'),
(31, 'plugins', '0002_auto_20210213_1553', '2021-02-13 12:53:55.286937'),
(32, 'plugins', '0003_plugins_id_in_rep', '2021-02-13 22:44:17.444969'),
(33, 'plugins', '0004_auto_20210214_2102', '2021-02-14 18:02:18.698069'),
(34, 'plugins', '0005_auto_20210214_2142', '2021-02-14 18:43:01.600795'),
(43, 'clients', '0001_initial', '2021-02-27 19:40:44.202178'),
(44, 'plugins', '0006_related', '2021-03-02 15:10:36.618942'),
(47, 'plugins', '0007_auto_20210302_2323', '2021-03-02 20:23:21.515233'),
(48, 'plugins', '0008_auto_20210302_2328', '2021-03-04 19:42:06.691579'),
(49, 'plugins', '0009_auto_20210304_2242', '2021-03-04 19:42:06.716581'),
(50, 'plugins', '0010_auto_20210304_2244', '2021-03-04 19:44:26.249561'),
(51, 'clients', '0002_auto_20210317_1213', '2021-03-17 09:13:29.883042'),
(53, 'plugins', '0011_plugins_related_class_name', '2021-03-17 11:59:20.819203'),
(55, 'money', '0001_initial', '2021-03-25 22:26:37.299030'),
(56, 'money', '0002_auto_20210329_0135', '2021-03-28 22:36:17.720626'),
(57, 'money', '0003_auto_20210329_0137', '2021-03-28 22:37:39.723316'),
(59, 'money', '0004_auto_20210330_1752', '2021-03-30 14:52:08.957019'),
(62, 'clients', '0003_auto_20210405_1354', '2021-04-05 10:55:01.540546'),
(65, 'orders', '0001_initial', '2021-04-30 22:53:49.112111'),
(66, 'orders', '0002_auto_20210501_0200', '2021-04-30 23:00:36.468411'),
(67, 'clients', '0004_auto_20210507_0129', '2021-05-06 22:30:43.165679'),
(68, 'clients', '0005_auto_20210509_0245', '2021-05-08 23:46:02.487167'),
(69, 'money', '0005_auto_20210509_0245', '2021-05-08 23:46:02.515169'),
(70, 'orders', '0003_auto_20210509_0245', '2021-05-08 23:46:02.650176'),
(71, 'prints', '0001_initial', '2021-07-16 20:51:20.828888'),
(72, 'clients', '0006_auto_20210722_0116', '2021-07-21 22:43:28.539015'),
(73, 'prints', '0002_auto_20210722_0143', '2021-07-21 22:43:28.545015'),
(74, 'prints', '0003_auto_20210723_0251', '2021-07-22 23:51:51.235514'),
(75, 'storehouse', '0001_initial', '2021-09-07 22:39:33.953897'),
(76, 'storehouse', '0002_auto_20210922_1910', '2021-09-22 16:10:46.054467'),
(77, 'storehouse', '0003_auto_20220108_1414', '2022-01-08 11:14:30.910112'),
(78, 'storehouse', '0004_auto_20220411_1416', '2022-04-11 11:16:26.238042');

-- --------------------------------------------------------

--
-- Структура таблицы `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1xc2y675xr4l10pdd0hpd7bm2v4h0tzv', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1n1Vpg:TseBO_oNEnOLcaxDvm8AXf3b31YHp-HrSK8gezrqJOg', '2022-01-09 15:53:12.552071'),
('5hcqecqpo18zj9523m2w6pazpmnt6hyk', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lOpFK:HUBeTgt3Y3VZSC267yPjVg0ai1TjF2iJf9BQP4yV2BA', '2021-04-06 22:11:30.201150'),
('5nk05i0fbfzk2sqzlvm0w95qkf45dqp7', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1labEB:n95kby68kmMZ_rvGrr29lRAoOacvaxeLeHOd3CRbJ3A', '2021-05-09 09:38:59.212766'),
('azq7dttx74af6pp3vf8hb64lk36h1pyo', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lFOc6:AQBWBL_ecvEYfyF1KoJHrWcRVNIEiO_L_EQeVxj8p2M', '2021-03-11 21:56:02.001024'),
('bbhyhc2sqdxqgpwkd8dljmr0pj92j115', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1llhRK:vilKjRHUgnSvihWwmRAiWaPVw3kB1-0X51XPWVcl63k', '2021-06-09 00:30:26.470989'),
('brd5okkuhreq4i1a31d59txpg8381tgc', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1mIfEl:Q0oDXggNcB6d-kpJg_a1teeYmo7YRngPxdATBj5aDtI', '2021-09-07 22:49:43.239452'),
('e2xwzql9u3db766q9otvsgrkmpn7kx0t', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1mNjQi:3fC_wmyQ7zU1_Vc2vz35CtACgyB2YbF3UM1ddHJXnHQ', '2021-09-21 22:19:00.729361'),
('e8uu7vm8bei62wzhjoocamlsyzqakfcg', '.eJxVjDsOwjAQBe_iGlmbjfGHkj5nsLzrNQkgR4qTCnF3iJQC2jcz76Vi2tYxbk2WOGV1UahOvxslfkjdQb6neps1z3VdJtK7og_a9DBneV4P9-9gTG381h2A8yYXZtebgtYhUS8pswfsHAUIRbiYznIPEjyCFaQMZxMK-2JJvT_gQzgC:1ndsY8:LqRbh478yHSKFVl4Ijv1uH7a8WX23SnBaI93IE5uW5A', '2022-04-25 11:49:40.594112'),
('erxsqn94c511k682j6webta3s11bm3q6', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1mJNSM:WCtHGXw2HKd7xI1ATmP09hQd1rbJ-1vi6asdvz_eg2o', '2021-09-09 22:02:42.449706'),
('fuzzrg7mwvjvwa1eq6tjfxshlgflul6j', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lz4AJ:yG4j5xU0keiGctVeyAwar9tHXsfeR56BkNXgjRWKSlA', '2021-07-15 21:24:07.333482'),
('fz8lxbep2hhp9ayz3uk1ow8kcrltb08v', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1m4Unf:fqkelLyJs9mFhPUJC-GLq4nrgmJFrydKlCcj83WF41o', '2021-07-30 20:51:11.198337'),
('i18t942ojrw4sbmjocbei25k70s7p8q0', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1m4St3:pW0Nzwj7yqEXSQZho8qrTC0qs-And8PuN-7jA6x6Vlc', '2021-07-30 18:48:37.984758'),
('i4o9o8jgyt4v1ok6fsf83ojs7c8xqqkx', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1l8iui:qvuA9Yd8rI3Jp9vGzWyRsPc51g1Mc4GhpFQRHhuYUOU', '2021-02-21 12:11:40.817190'),
('n1r5abjcjjghtwnyrmfvy21qla5kp60d', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lAuJm:X_rguXlIVZC5kk8ysZpE96Sa0DXS18oVk4UsviEcpOU', '2021-02-27 12:46:34.974753'),
('n7l47olppwwo4payd119u7jsf8t91yo6', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1mlZef:o-92-O5K-U-MDkXukpqblp9xCyAHfKOOU3_8kQELbAw', '2021-11-26 16:43:57.145897'),
('onqiawdiophqz9r7pvqa6nxuenjpybsb', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1mmzqK:gfBJl3XqTArMb2Uzo4LbDlBUi7qRy6zdjyD6yyKFebA', '2021-11-30 14:53:52.985852'),
('oodkzf2vnlgz5sswl91k2tl49e1c8i25', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lG4g2:8Dbfm1LipftFFm28u463ZNemUnv7PkUHG38fBUlnhQE', '2021-03-13 18:50:54.247163'),
('opc0owfko59rwfrbxgv1hxg7jrnu1vgv', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1n9Bkd:QA-9z0Kz5ncc55Kva44b5Lml3gzYbMqB6Dy7dMHeJFo', '2022-01-30 20:03:43.647987'),
('otmwuj4qcb4mgrf709rddrv331sjm8o8', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lAhpI:w1K91vZlho5Uoo1_8ZmEprSkQWxf0ROmj7mSI6ODB3Q', '2021-02-26 23:26:16.102230'),
('oy61kly2jdiwwuqewm6daprkq96rqlkn', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lgb4L:U7VDKvhF4fc1of5dIcRH-DLQ5qF-y0AxC5fgrIbXR_0', '2021-05-25 22:41:37.932261'),
('ph0o8hi5o8cmh6c0o47em7xe6sfkpz5v', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1l73vC:UOKHQJKZNci5NACNQv43ZuXYOwmROv3wYnGHOnBn1OY', '2021-02-16 22:13:18.956899'),
('pwgv1gr4jgoc105qg00jmkb3cz6ef54f', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lBGHY:v_an9uq3sH9-6BYIKyBZbTkyzXR1RXID6C78xGEpfog', '2021-02-28 12:13:44.175827'),
('s3novr0hkm619cb1fhln0rthqt5qh56m', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1m4UUo:p9lS_QbcFTBJ7QMh7udbsGpXIFcQqsHJl9bkHw_kKuE', '2021-07-30 20:31:42.613498'),
('sgag5iwdktsghqr83rr7xo4c1g1cagfc', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1mcuqw:xfbUnK_b6L6MswpL0csaWoS9g7zxVVhuaWUPYC3Oqy8', '2021-11-02 19:32:50.663590'),
('shwx7z7e3d0krwvsplyxam5416ubodfa', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lB3Jp:2_JNhxc02S_MWbGVeVmeVxHNlpMEG5tyBLxmaUv-v_Y', '2021-02-27 22:23:13.562679'),
('swrygwbmus0iwvz1ycbjis2clzxkpxv4', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lsXsV:QlHhvn2sIC-0Z5WuTdPpyc3Kz6xDkbw5K1s2hNoJyMs', '2021-06-27 21:42:47.600990'),
('tvuq0fck5fy8b60dst7o4movptwgbyek', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lAMKK:Lt_ZHDGmiSk94gL_PmUiXxZpvx3erXemKX6R7kW_pIo', '2021-02-26 00:28:52.218270'),
('udj0fs4wr63dacnj8a9mo1tv5o1tch48', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lB2m3:Biuk1rrC-CznzKa9pclBepnqFVm7QhXMw6-LqVuglaA', '2021-02-27 21:48:19.809923'),
('uk25boaex484najahsr1b3y9j4isujzs', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lVKNY:wp7tDrPfnHrtcaFL2O9firm_O7ZYamBwLz_ACj_T7vU', '2021-04-24 20:38:52.947429'),
('vec1x24soo76ozz1c5mfrla50esjlvba', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1mNjjT:nsHjXiMtU0d0QmR954zh01_G0rQ4rrkDrhmgKrW1Gw4', '2021-09-21 22:38:23.930892'),
('vom27hi6im65kcd64w0wuf3mdjbyano1', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lJhOd:94paJ1-YIfXJ0Y6qjISxC-dhosqu9lS4BtspeANxLoQ', '2021-03-23 18:47:55.713115'),
('x3zfb774thzmlcfuoz22hwwjzqrmpa7p', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lG51p:yczSfbJ2pgIrmsbzrfLE-8fFaRXagrVOJROatisw1v0', '2021-03-13 19:13:25.272437'),
('x5vwv8e0trp7duht12jc1ru7d1j2tyta', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1mJPW2:8fV0m25lrHxucUBgHKuss16oiEk5Q9KHpsLERw_Hol0', '2021-09-10 00:14:38.949504'),
('x9odqruifrq193qurq4rpfre810sxzle', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1mCU0J:5E0YJzJVc8hTj1CojzFIfpPrKPWp8ZieIHVXUWyUl3M', '2021-08-21 21:37:15.261846'),
('xgo3wc4eblkrcxarg4d3fgixr9ke1a0a', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1m4Um8:tCvgPvO-M4l8rcvZ8k8X8FbGm5PBsJJ-fAvga0QulRk', '2021-07-30 20:49:36.758936'),
('xsflvkzvbjer6zdgbk3aheabhy4vswe7', '.eJxVjMEOwiAQRP-FsyFlKVA9evcbyMIuUjWQlPZk_Hdp0oMeZ96beQuP25r91njxM4mLUOL02wWMTy47oAeWe5WxlnWZg9wVedAmb5X4dT3cv4OMLff1BGQwgR05pfNITpMF05NyMaqgTQxKB8XQPQvgJm0ZB4cuDkQmWRCfL-PkN84:1lPvrk:rx-5915qtLGJ6U1MQFBb4PZjJd_K6rd-aDJKSK0XBTE', '2021-04-09 23:27:44.613010');

-- --------------------------------------------------------

--
-- Структура таблицы `money_money`
--

CREATE TABLE `money_money` (
  `id` int(11) NOT NULL,
  `money` decimal(19,2) NOT NULL,
  `prepayment` decimal(19,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `related_uuid` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL
) ;

--
-- Дамп данных таблицы `money_money`
--

INSERT INTO `money_money` (`id`, `money`, `prepayment`, `created_at`, `updated_at`, `related_uuid`) VALUES
(23, '100.00', '100.00', '2021-05-08 23:59:52.854661', '2021-05-08 23:59:52.854661', '{\"4M8XnFY8ybMG9ucum6JyFW\": \"\"}'),
(24, '0.00', '0.00', '2021-05-13 01:01:56.194360', '2021-05-13 01:01:56.195360', '{\"McbMAr4iTZ7bArBGmcPY3M\": \"\"}'),
(25, '0.00', '0.00', '2021-05-13 01:05:37.128997', '2021-05-13 01:05:37.128997', '{\"JbAHMMHnwyEVM3cPjRWRcA\": \"\"}'),
(26, '999.00', '999.00', '2021-05-14 22:13:58.846621', '2021-05-15 00:24:37.493966', '{\"Ex7bjyiyEfnyg7q4oKcAzo\": \"\"}'),
(27, '1111199.00', '123213.00', '2021-05-17 22:53:22.103130', '2021-05-20 23:05:55.823100', '{\"EK9ZduAavU7LNLgz5JNwW7\": \"\"}'),
(29, '666.00', '666.00', '2021-05-29 22:11:54.280137', '2021-05-29 22:11:54.280137', '{\"S5t3DEcADfA3JgaZAK5dNG\": \"\"}'),
(30, '666.00', '666.00', '2021-06-02 22:12:29.325615', '2021-06-02 22:12:29.325615', '{\"55EoLaFncaDDkDbFAeJhe2\": \"\"}'),
(31, '1.00', '1.00', '2021-07-06 22:02:14.021774', '2021-07-06 22:02:14.021774', '{\"K664eDqzNvkrVSLRoQsYDt\": \"\"}'),
(32, '1.00', '1.00', '2021-07-06 22:05:41.353632', '2021-07-06 22:05:41.353632', '{\"9rbFPz27Y83rztFGPkdStk\": \"\"}'),
(33, '0.00', '0.00', '2021-07-06 22:09:05.841328', '2021-07-06 22:09:05.841328', '{\"H6xEH34H9wgv9BekvSvHKA\": \"\"}'),
(34, '0.00', '0.00', '2021-07-06 22:09:52.642005', '2021-07-06 22:09:52.642005', '{\"5WdWqkRgwcXmEViTHoZnce\": \"\"}'),
(35, '0.00', '0.00', '2021-07-12 21:59:11.008538', '2021-07-12 21:59:11.008538', '{\"k9vLs7CqZaipigeouUtETZ\": \"\"}'),
(36, '0.00', '0.00', '2021-07-12 21:59:35.981966', '2021-07-12 21:59:35.982966', '{\"o53hfjYQymdV8DjCe4ANAo\": \"\"}'),
(37, '10.00', '0.00', '2021-07-12 23:09:10.233720', '2021-12-26 17:52:44.362088', '{\"PS7LRcCVsf83BKHZZPAeRk\": \"\"}'),
(38, '0.00', '0.00', '2022-01-16 22:04:27.506312', '2022-01-16 22:04:27.506312', '{\"Dyqg8eT8BjGVp74nJcgmDm\": \"\"}');

-- --------------------------------------------------------

--
-- Структура таблицы `news_category`
--

CREATE TABLE `news_category` (
  `id` int(11) NOT NULL,
  `title` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `news_category`
--

INSERT INTO `news_category` (`id`, `title`) VALUES
(1, 'Культура'),
(2, 'Политика');

-- --------------------------------------------------------

--
-- Структура таблицы `news_news`
--

CREATE TABLE `news_news` (
  `id` int(11) NOT NULL,
  `title` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `photo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `category_id` int(11) NOT NULL,
  `views` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `news_news`
--

INSERT INTO `news_news` (`id`, `title`, `content`, `created_at`, `updated_at`, `photo`, `is_published`, `category_id`, `views`) VALUES
(1, '123', '123', '2021-02-04 11:54:28.131731', '2021-02-07 12:33:17.256342', 'photos/2021/02/07/zSn2zPflRBw.jpg', 1, 1, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `orders_category`
--

CREATE TABLE `orders_category` (
  `id` int(11) NOT NULL,
  `title` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `orders_category`
--

INSERT INTO `orders_category` (`id`, `title`, `category`) VALUES
(1, 'fast', 'fast'),
(2, 'simple', 'simple');

-- --------------------------------------------------------

--
-- Структура таблицы `orders_device`
--

CREATE TABLE `orders_device` (
  `id` int(11) NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `used` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `orders_device`
--

INSERT INTO `orders_device` (`id`, `name`, `used`) VALUES
(1, 'Слава', 0),
(2, 'Восток', 0),
(3, 'Casio', 2),
(4, 'выавыа', 0),
(5, 'Casio Edifice', 3),
(6, 'Casio G-Shock', 4),
(7, 'Appella', 1),
(8, 'Diesel', 0),
(9, 'Tissot', 5);

-- --------------------------------------------------------

--
-- Структура таблицы `orders_orders`
--

CREATE TABLE `orders_orders` (
  `id` int(11) NOT NULL,
  `serial` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `comment` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `related_uuid` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `category_id` int(11) NOT NULL,
  `device_id` int(11) NOT NULL,
  `related_user_id` int(11) DEFAULT NULL,
  `service_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL
) ;

--
-- Дамп данных таблицы `orders_orders`
--

INSERT INTO `orders_orders` (`id`, `serial`, `comment`, `created_at`, `updated_at`, `related_uuid`, `category_id`, `device_id`, `related_user_id`, `service_id`, `status_id`) VALUES
(16, 'zzz', 'zzz', '2021-05-08 23:59:52.773657', '2021-07-13 22:52:58.428215', '{\"4M8XnFY8ybMG9ucum6JyFW\": \"\"}', 2, 4, 1, 1, 2),
(17, '', '', '2021-05-13 00:45:10.775853', '2021-05-13 00:45:10.775853', '{\"JNVDPK9mLGf9DWeDfWQgDa\": \"\"}', 2, 4, 1, 3, 1),
(18, '', '', '2021-05-13 00:45:28.870888', '2021-05-13 00:45:28.870888', '{\"bmrhXVhiABLvGFtq2zCKZW\": \"\"}', 2, 4, 1, 3, 1),
(19, '', '', '2021-05-13 00:56:27.791576', '2021-05-13 00:56:27.791576', '{\"G8gcMtMfoijY6hyHkwUbVa\": \"\"}', 2, 4, 1, 3, 1),
(20, '', '', '2021-05-13 00:57:41.103769', '2021-05-13 00:57:41.103769', '{\"4PpQdUQrEsiaMNKBP8DHM4\": \"\"}', 2, 4, 1, 3, 1),
(21, '', '', '2021-05-13 00:58:42.463279', '2021-05-13 00:58:42.463279', '{\"CQA4nFtfjTG7SAMagKzQLa\": \"\"}', 2, 4, 1, 3, 1),
(22, '', '', '2021-05-13 01:01:56.141357', '2021-05-13 01:01:56.141357', '{\"McbMAr4iTZ7bArBGmcPY3M\": \"\"}', 2, 4, 1, 3, 1),
(23, '', '', '2021-05-13 01:05:37.073993', '2021-05-13 01:05:37.073993', '{\"JbAHMMHnwyEVM3cPjRWRcA\": \"\"}', 2, 4, 1, 3, 1),
(24, 'asdasd', 'asdasdtest', '2021-05-14 22:13:58.782617', '2021-05-15 00:24:37.463964', '{\"Ex7bjyiyEfnyg7q4oKcAzo\": \"\"}', 2, 4, 1, 3, 2),
(25, 'яяяяяяяяяя', 'aaaяяя', '2021-05-17 22:53:22.075128', '2021-05-20 23:05:55.796098', '{\"EK9ZduAavU7LNLgz5JNwW7\": \"\"}', 2, 3, 1, 3, 1),
(26, '', 'zzz', '2021-05-29 22:11:07.276449', '2021-05-29 22:11:07.276449', '{\"oNjPHdEeBNrR8FtZfuDR5T\": \"\"}', 1, 4, 1, 3, 1),
(27, '', 'zzz', '2021-05-29 22:11:54.214133', '2021-05-29 22:11:54.214133', '{\"S5t3DEcADfA3JgaZAK5dNG\": \"\"}', 1, 4, 1, 3, 1),
(28, '', 'asdsadsad', '2021-06-02 22:12:29.273612', '2021-06-02 22:12:29.273612', '{\"55EoLaFncaDDkDbFAeJhe2\": \"\"}', 1, 1, 1, 1, 1),
(29, '', '', '2021-07-06 22:02:13.963770', '2021-07-06 22:02:13.963770', '{\"K664eDqzNvkrVSLRoQsYDt\": \"\"}', 2, 4, 1, 3, 1),
(30, '', '', '2021-07-06 22:05:41.295629', '2021-07-06 22:05:41.295629', '{\"9rbFPz27Y83rztFGPkdStk\": \"\"}', 2, 1, 1, 2, 1),
(31, '', '', '2021-07-06 22:09:05.775325', '2021-07-06 22:09:05.775325', '{\"H6xEH34H9wgv9BekvSvHKA\": \"\"}', 2, 2, 1, 3, 1),
(32, '', '', '2021-07-06 22:09:52.587002', '2021-07-06 22:09:52.587002', '{\"5WdWqkRgwcXmEViTHoZnce\": \"\"}', 2, 1, 1, 3, 1),
(33, '', '', '2021-07-12 21:59:10.978536', '2021-07-12 21:59:10.978536', '{\"k9vLs7CqZaipigeouUtETZ\": \"\"}', 2, 4, 1, 2, 1),
(34, '', '', '2021-07-12 21:59:35.956965', '2021-07-12 21:59:35.956965', '{\"o53hfjYQymdV8DjCe4ANAo\": \"\"}', 2, 7, 1, 2, 1),
(35, '', '', '2021-07-12 23:09:10.179717', '2021-12-26 17:52:44.336087', '{\"PS7LRcCVsf83BKHZZPAeRk\": \"\"}', 2, 9, 1, 1, 1),
(36, '123', 'qwe', '2022-01-16 22:04:27.476310', '2022-01-16 22:04:27.476310', '{\"Dyqg8eT8BjGVp74nJcgmDm\": \"\"}', 2, 3, 1, 1, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `orders_service`
--

CREATE TABLE `orders_service` (
  `id` int(11) NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `used` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `orders_service`
--

INSERT INTO `orders_service` (`id`, `name`, `used`) VALUES
(1, 'Замена батареек', 0),
(2, 'Замена стекла', 0),
(3, 'Замена ушка', 0);

-- --------------------------------------------------------

--
-- Структура таблицы `orders_status`
--

CREATE TABLE `orders_status` (
  `id` int(11) NOT NULL,
  `title` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `orders_status`
--

INSERT INTO `orders_status` (`id`, `title`) VALUES
(2, 'Выдано'),
(3, 'Отказ'),
(1, 'Принято');

-- --------------------------------------------------------

--
-- Структура таблицы `plugins_plugins`
--

CREATE TABLE `plugins_plugins` (
  `id` int(11) NOT NULL,
  `title` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `module_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `version` int(11) NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `photo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `category_id` int(11) NOT NULL,
  `is_migrate` tinyint(1) NOT NULL,
  `id_in_rep` int(11) NOT NULL,
  `related_class_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `plugins_plugins`
--

INSERT INTO `plugins_plugins` (`id`, `title`, `module_name`, `version`, `description`, `photo`, `is_active`, `category_id`, `is_migrate`, `id_in_rep`, `related_class_name`) VALUES
(41, 'Заказы', 'orders', 1, 'Плагин работы с заказами клиентов', 'http://127.0.0.1:8001/media/photos/2021/02/06/zSn2zPflRBw_qLb3uNP.jpg', 1, 1, 0, 12, 'Orders'),
(43, 'Клиенты', 'clients', 1, 'Плагин для работы с базой клиентов', 'http://127.0.0.1:8001/media/photos/2021/02/26/1413.png', 1, 1, 0, 14, 'Clients'),
(44, 'Бухгалтерия', 'money', 1, 'Деньги', 'http://127.0.0.1:8001/media/photos/2021/03/26/photo_1529595_56544df57b2f0.jpg', 1, 1, 0, 15, 'Money'),
(48, 'Печать', 'prints', 1, 'Печатные данные для заказов итд', 'http://127.0.0.1:8001/media/photos/2021/07/16/5k8Iv1U43TRemZvdP.jpg', 1, 1, 0, 16, 'Prints'),
(49, 'Отделения', 'storehouse', 1, 'Отделения', 'http://127.0.0.1:8001/media/photos/2021/08/27/metmebel.jpg', 1, 1, 0, 17, 'StoreRelated');

-- --------------------------------------------------------

--
-- Структура таблицы `plugins_pluginscategory`
--

CREATE TABLE `plugins_pluginscategory` (
  `id` int(11) NOT NULL,
  `title` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `plugins_pluginscategory`
--

INSERT INTO `plugins_pluginscategory` (`id`, `title`) VALUES
(1, 'Test');

-- --------------------------------------------------------

--
-- Структура таблицы `plugins_plugins_related`
--

CREATE TABLE `plugins_plugins_related` (
  `id` int(11) NOT NULL,
  `from_plugins_id` int(11) NOT NULL,
  `to_plugins_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `plugins_plugins_related`
--

INSERT INTO `plugins_plugins_related` (`id`, `from_plugins_id`, `to_plugins_id`) VALUES
(33, 41, 43),
(36, 41, 44),
(45, 41, 48),
(50, 41, 49),
(34, 43, 41),
(41, 43, 48),
(35, 44, 41),
(48, 44, 48),
(46, 48, 41),
(38, 48, 43),
(47, 48, 44),
(49, 49, 41);

-- --------------------------------------------------------

--
-- Структура таблицы `prints_prints`
--

CREATE TABLE `prints_prints` (
  `id` int(11) NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contentform` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `related_uuid` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `prints_prints`
--

INSERT INTO `prints_prints` (`id`, `name`, `contentform`, `related_uuid`) VALUES
(1, 'test', '<p><u><em><strong>test</strong></em></u></p>', NULL),
(2, 'Чек телефоны', '<p><u><em><strong>test</strong></em></u></p>', NULL),
(3, 'Чек часы', '<p>&nbsp;</p>\r\n\r\n<p><strong>Номер заказа:</strong>&nbsp;orders.Orders.id</p>\r\n\r\n<p><strong>Создан:&nbsp;</strong>orders.Orders.created_at</p>\r\n\r\n<p><strong>Устройство:</strong>&nbsp;orders.Orders.device</p>\r\n\r\n<p><strong>Услуга:</strong>&nbsp;orders.Orders.service</p>\r\n\r\n<p><strong>Серийник:</strong> orders.Orders.serial</p>\r\n\r\n<p><strong>Клиент:</strong>&nbsp;clients.Clients.name</p>\r\n\r\n<p><strong>Телефон:</strong>&nbsp;clients.Clients.phone</p>\r\n\r\n<p><strong>Денег:</strong>&nbsp;money.Money.money</p>\r\n\r\n<p><strong>Предоплата:</strong>&nbsp;money.Money.prepayment</p>', NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `storehouse_category`
--

CREATE TABLE `storehouse_category` (
  `id` int(11) NOT NULL,
  `title` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `storehouse_category`
--

INSERT INTO `storehouse_category` (`id`, `title`) VALUES
(4, 'Курьер'),
(3, 'Склад'),
(5, 'Точка');

-- --------------------------------------------------------

--
-- Структура таблицы `storehouse_storehouses`
--

CREATE TABLE `storehouse_storehouses` (
  `id` int(11) NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(17) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category_id` int(11) NOT NULL,
  `related_user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `storehouse_storehouses`
--

INSERT INTO `storehouse_storehouses` (`id`, `name`, `address`, `phone`, `category_id`, `related_user_id`) VALUES
(1, 'Купчино', 'Балканская пл. 5', '+79211234567', 5, NULL);

-- --------------------------------------------------------

--
-- Структура таблицы `storehouse_storerelated`
--

CREATE TABLE `storehouse_storerelated` (
  `id` int(11) NOT NULL,
  `related_uuid` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`related_uuid`)),
  `store_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `storehouse_storerelated`
--

INSERT INTO `storehouse_storerelated` (`id`, `related_uuid`, `store_id`) VALUES
(1, '12345', 1),
(2, '{\"Dyqg8eT8BjGVp74nJcgmDm\": \"\"}', 1);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Индексы таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Индексы таблицы `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Индексы таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Индексы таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Индексы таблицы `clients_clients`
--
ALTER TABLE `clients_clients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `clients_clients_phone_925efed4_uniq` (`phone`);

--
-- Индексы таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Индексы таблицы `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Индексы таблицы `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Индексы таблицы `money_money`
--
ALTER TABLE `money_money`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `news_category`
--
ALTER TABLE `news_category`
  ADD PRIMARY KEY (`id`),
  ADD KEY `news_category_title_175a164c` (`title`);

--
-- Индексы таблицы `news_news`
--
ALTER TABLE `news_news`
  ADD PRIMARY KEY (`id`),
  ADD KEY `news_news_category_id_f060a768_fk_news_category_id` (`category_id`);

--
-- Индексы таблицы `orders_category`
--
ALTER TABLE `orders_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `orders_category_category_7b362cd9_uniq` (`category`);

--
-- Индексы таблицы `orders_device`
--
ALTER TABLE `orders_device`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `orders_orders`
--
ALTER TABLE `orders_orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `orders_orders_category_id_94ac90da_fk_orders_category_id` (`category_id`),
  ADD KEY `orders_orders_related_user_id_dfc3d047_fk_auth_user_id` (`related_user_id`),
  ADD KEY `orders_orders_status_id_d38b6b06_fk_orders_status_id` (`status_id`),
  ADD KEY `orders_orders_device_id_3f2aa708_fk_orders_device_id` (`device_id`),
  ADD KEY `orders_orders_service_id_899e1a80_fk_orders_service_id` (`service_id`);

--
-- Индексы таблицы `orders_service`
--
ALTER TABLE `orders_service`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Индексы таблицы `orders_status`
--
ALTER TABLE `orders_status`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `orders_status_title_5b54f2f8_uniq` (`title`);

--
-- Индексы таблицы `plugins_plugins`
--
ALTER TABLE `plugins_plugins`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plugins_plugins_category_id_b93592ae_fk_plugins_p` (`category_id`);

--
-- Индексы таблицы `plugins_pluginscategory`
--
ALTER TABLE `plugins_pluginscategory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plugins_category_title_251e06a5` (`title`);

--
-- Индексы таблицы `plugins_plugins_related`
--
ALTER TABLE `plugins_plugins_related`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `plugins_plugins_related_from_plugins_id_to_plugi_c007f649_uniq` (`from_plugins_id`,`to_plugins_id`),
  ADD KEY `plugins_plugins_rela_to_plugins_id_07b17fa8_fk_plugins_p` (`to_plugins_id`);

--
-- Индексы таблицы `prints_prints`
--
ALTER TABLE `prints_prints`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `storehouse_category`
--
ALTER TABLE `storehouse_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `storehouse_category_title_ecdd2d64_uniq` (`title`);

--
-- Индексы таблицы `storehouse_storehouses`
--
ALTER TABLE `storehouse_storehouses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD KEY `storehouse_storehous_category_id_2ff6334c_fk_storehous` (`category_id`),
  ADD KEY `storehouse_storehouses_related_user_id_61b293ec_fk_auth_user_id` (`related_user_id`);

--
-- Индексы таблицы `storehouse_storerelated`
--
ALTER TABLE `storehouse_storerelated`
  ADD PRIMARY KEY (`id`),
  ADD KEY `storehouse_storerela_store_id_ddf76ec5_fk_storehous` (`store_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=117;

--
-- AUTO_INCREMENT для таблицы `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=158;

--
-- AUTO_INCREMENT для таблицы `clients_clients`
--
ALTER TABLE `clients_clients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=128;

--
-- AUTO_INCREMENT для таблицы `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT для таблицы `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT для таблицы `money_money`
--
ALTER TABLE `money_money`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `news_category`
--
ALTER TABLE `news_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `news_news`
--
ALTER TABLE `news_news`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `orders_category`
--
ALTER TABLE `orders_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `orders_device`
--
ALTER TABLE `orders_device`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `orders_orders`
--
ALTER TABLE `orders_orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `orders_service`
--
ALTER TABLE `orders_service`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `orders_status`
--
ALTER TABLE `orders_status`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `plugins_plugins`
--
ALTER TABLE `plugins_plugins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- AUTO_INCREMENT для таблицы `plugins_pluginscategory`
--
ALTER TABLE `plugins_pluginscategory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `plugins_plugins_related`
--
ALTER TABLE `plugins_plugins_related`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT для таблицы `prints_prints`
--
ALTER TABLE `prints_prints`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `storehouse_category`
--
ALTER TABLE `storehouse_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `storehouse_storehouses`
--
ALTER TABLE `storehouse_storehouses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `storehouse_storerelated`
--
ALTER TABLE `storehouse_storerelated`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `news_news`
--
ALTER TABLE `news_news`
  ADD CONSTRAINT `news_news_category_id_f060a768_fk_news_category_id` FOREIGN KEY (`category_id`) REFERENCES `news_category` (`id`);

--
-- Ограничения внешнего ключа таблицы `orders_orders`
--
ALTER TABLE `orders_orders`
  ADD CONSTRAINT `orders_orders_category_id_94ac90da_fk_orders_category_id` FOREIGN KEY (`category_id`) REFERENCES `orders_category` (`id`),
  ADD CONSTRAINT `orders_orders_device_id_3f2aa708_fk_orders_device_id` FOREIGN KEY (`device_id`) REFERENCES `orders_device` (`id`),
  ADD CONSTRAINT `orders_orders_related_user_id_dfc3d047_fk_auth_user_id` FOREIGN KEY (`related_user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `orders_orders_service_id_899e1a80_fk_orders_service_id` FOREIGN KEY (`service_id`) REFERENCES `orders_service` (`id`),
  ADD CONSTRAINT `orders_orders_status_id_d38b6b06_fk_orders_status_id` FOREIGN KEY (`status_id`) REFERENCES `orders_status` (`id`);

--
-- Ограничения внешнего ключа таблицы `plugins_plugins`
--
ALTER TABLE `plugins_plugins`
  ADD CONSTRAINT `plugins_plugins_category_id_b93592ae_fk_plugins_p` FOREIGN KEY (`category_id`) REFERENCES `plugins_pluginscategory` (`id`);

--
-- Ограничения внешнего ключа таблицы `plugins_plugins_related`
--
ALTER TABLE `plugins_plugins_related`
  ADD CONSTRAINT `plugins_plugins_rela_from_plugins_id_51f604ea_fk_plugins_p` FOREIGN KEY (`from_plugins_id`) REFERENCES `plugins_plugins` (`id`),
  ADD CONSTRAINT `plugins_plugins_rela_to_plugins_id_07b17fa8_fk_plugins_p` FOREIGN KEY (`to_plugins_id`) REFERENCES `plugins_plugins` (`id`);

--
-- Ограничения внешнего ключа таблицы `storehouse_storehouses`
--
ALTER TABLE `storehouse_storehouses`
  ADD CONSTRAINT `storehouse_storehous_category_id_2ff6334c_fk_storehous` FOREIGN KEY (`category_id`) REFERENCES `storehouse_category` (`id`),
  ADD CONSTRAINT `storehouse_storehouses_related_user_id_61b293ec_fk_auth_user_id` FOREIGN KEY (`related_user_id`) REFERENCES `auth_user` (`id`);

--
-- Ограничения внешнего ключа таблицы `storehouse_storerelated`
--
ALTER TABLE `storehouse_storerelated`
  ADD CONSTRAINT `storehouse_storerela_store_id_ddf76ec5_fk_storehous` FOREIGN KEY (`store_id`) REFERENCES `storehouse_storehouses` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
