# This Puppet manifest installs and configures Nginx to serve a 'Hello World!' page and redirect '/redirect_me' with a 301 response.
class nginx_setup {
  package { 'nginx':
    ensure => installed,
  }

  service { 'nginx':
    ensure     => running,
    enable     => true,
    require    => Package['nginx'],
  }

  file { '/var/www/html/index.html':
    ensure  => file,
    content => '<html>\n<head>\n<title>Hello World
