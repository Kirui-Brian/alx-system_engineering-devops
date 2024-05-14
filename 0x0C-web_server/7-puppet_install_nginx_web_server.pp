# This Puppet manifest installs and configures Nginx to serve a 'Hello World!' page and redirect '/redirect_me' with a 301 response.
class nginx_setup {
  package { 'nginx':
    ensure => installed,
    before => File['/var/www/html/index.html'],
  }

  service { 'nginx':
    ensure     => running,
    enable     => true,
    require    => Package['nginx'],
    subscribe  => File['/var/www/html/index.html', '/etc/nginx/sites-available/default'],
  }

  file { '/var/www/html/index.html':
    ensure  => file,
    content => 'Hello World!\n',
    require => Package['nginx'],
  }

  file { '/etc/nginx/sites-available/default':
    ensure  => file,
    content => template('nginx/default.erb'),
    require => Package['nginx'],
  }
}

include nginx_setup

# Template file: nginx/default.erb
# Place this template in the appropriate Puppet module directory
<% | $redirect_url = 'http://google.com/' |%>
server {
  listen 80;
  listen [::]:80 default_server;
  root   /var/www/html;
  index  index.html index.htm index.nginx-debian.html;

  location / {
    try_files $uri $uri/ =404;
  }

  location /redirect_me {
    return 301 <%= $redirect_url %>;
  }
}
