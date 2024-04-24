# 使用 Nginx 作为基础镜像
FROM nginx

# 将当前目录下的 dist 文件夹内容复制到 Nginx 默认的静态文件目录
COPY ./dist /usr/share/nginx/html

# 暴露容器的 80 端口
EXPOSE 80