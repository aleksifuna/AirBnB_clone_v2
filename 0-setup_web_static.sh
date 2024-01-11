#!/usr/bin/env bash
# Install Nginx if not ready installed
# create folder /data/ if if doesnt exist
# create folder /data/web_static if it doesnt exist
# create folder /data/web_static/release/ if it doesnt exist
# create folder /data/web_static/shared/ if it doesnt exist
# create folder /data/web_static/release/test if it doesnt exist
# creates /data/web_static/release/test/index.html
# creates a symbolic link /data/web_static/current linked to the
# /data/web_static/release/test/ folder.
# change ownership of /data/ to ubuntu user


apt-get update
apt-get install -y nginx
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/release/test/

cat > /data/web_static/release/test/index.html <<EOF
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

if [ -L /data/web_static/current ]; then
        rm /data/web_static/current
fi

ln -s /data/web_static/release/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data

cat > /etc/nginx/sites-available/default <<EOF
server {
	listen 80;
	listen [::]:80 default_server;
	root   /data/web_static/current;
	index  index.html index.htm;
	location / {
        try_files \$uri \$uri/ =404;
	add_header X-Served-By \$HOSTNAME;
    }
	location /hbnb_static {
	alias /data/web_static/current/;
	try_files \$uri \$uri/ =404;
        add_header X-Served-By \$HOSTNAME;
	}
}
EOF

service nginx restart
