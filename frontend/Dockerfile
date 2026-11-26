# Берем готовый образ веб-сервера Nginx (он очень легкий)
FROM nginx:alpine

# Копируем нашу HTML-страницу в папку, откуда Nginx раздает сайты
COPY index.html /usr/share/nginx/html/index.html

# Копируем настройки Nginx (чтобы он передавал запросы на сервер)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Говорим, что контейнер работает на 80 порту
EXPOSE 80