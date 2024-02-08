-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 08-02-2024 a las 22:17:40
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `aplicacionweb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `correo` varchar(55) NOT NULL,
  `nombreUsuario` varchar(20) NOT NULL,
  `contraseña` varchar(100) NOT NULL,
  `fotoUsuario` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`correo`, `nombreUsuario`, `contraseña`, `fotoUsuario`) VALUES
('abetancurquintero066@gmail.com', 'CP9', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'E20231010152837.jpg'),
('isabellaruiz948@gmail.com', 'Isabella', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'E20231225124244.png'),
('jhona@gmail.com', 'JHONA', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'E20231010210232.png'),
('jhonagc78@gmail.com', 'alexis', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'E20231225131349.png'),
('salchichon@gmail.com', 'TYK', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'E20231010155936.png'),
('toby1@gmail.com', 'TOBY', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'E20231010210707.png');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `videos`
--

CREATE TABLE `videos` (
  `correoUsuario` varchar(50) NOT NULL,
  `nombreUsuario` varchar(20) NOT NULL,
  `nombreVideo` varchar(50) NOT NULL,
  `portada` varchar(70) NOT NULL,
  `video` varchar(80) NOT NULL,
  `FotoUsuario` varchar(80) DEFAULT NULL,
  `fechaSubida` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `videos`
--

INSERT INTO `videos` (`correoUsuario`, `nombreUsuario`, `nombreVideo`, `portada`, `video`, `FotoUsuario`, `fechaSubida`) VALUES
('abetancurquintero066@gmail.com', 'CP9', 'when subes el primer video a tu plataforma web', 'E20231013222302.jpg', 'V20231013222302.mp4', 'E20231010152837.jpg', '2006-03-03'),
('abetancurquintero066@gmail.com', 'CP9', 'When subes el segundo video a tu plataforma web', 'E20231015212059.jpg', 'V20231015212058.mp4', 'E20231010152837.jpg', '2006-03-03'),
('abetancurquintero066@gmail.com', 'CP9', 'when subes el tercer video a tu plataforma web', 'E20231015214849.jpg', 'V20231015214849.mp4', 'E20231010152837.jpg', '2006-03-03'),
('abetancurquintero066@gmail.com', 'CP9', 'when subes el cuarto video a tu plataforma web', 'E20231016161834.jpg', 'V20231016161834.mp4', 'E20231010152837.jpg', '2006-03-03'),
('toby1@gmail.com', 'TOBY', 'when subes el quinto video a tu plataforma web', 'E20231016170545.jpg', 'V20231016170545.mp4', 'E20231010210707.png', '2006-03-03'),
('abetancurquintero066@gmail.com', 'CP9', 'when subes el sexto video a tu plataforma web', 'E20231018205554.jpg', 'V20231018205554.mp4', 'E20231010152837.jpg', '2023-10-18');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`correo`);

--
-- Indices de la tabla `videos`
--
ALTER TABLE `videos`
  ADD KEY `fkcorreoUsuario` (`correoUsuario`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `videos`
--
ALTER TABLE `videos`
  ADD CONSTRAINT `fkcorreoUsuario` FOREIGN KEY (`correoUsuario`) REFERENCES `usuarios` (`correo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
