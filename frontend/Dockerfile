# Берем готовый образ веб-сервера Nginx конкретной версии
FROM nginx:alpine

# Копируем нашу HTML-страницу в папку докера, откуда Nginx раздает сайты
COPY index.html /usr/share/nginx/html/index.html

# Копируем настройки Nginx (чтобы он передавал запросы на сервер)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Говорим, что контейнер работает по 80 порту (наш 8123)
EXPOSE 80