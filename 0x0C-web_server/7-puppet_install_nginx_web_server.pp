# Puppet manifest to install and configure Nginx with a 301 redirect for /redirect_me

class nginx_setup {
  package { 'nginx':
    ensure => installed,
    before => File['/var/www/html/index.html'],
  }

  file { '/var/www/html/index.html':
    ensure  => file,
    content => 'Hello World!\n',
    require => Package['nginx'],
  }

  file { '/var/www/html/404.html':
    ensure  => file,
    content => "Ceci n'est pas une page\n",
    require => Package['nginx'],
  }

  file { '/etc/nginx/sites-available/default':
    ensure  => file,
    content => template('nginx/default.conf.erb'),
    require => Package['nginx'],
    notify  => Service['nginx'],
  }

  service { 'nginx':
    ensure    => running,
    enable    => true,
    subscribe => File['/etc/nginx/sites-available/default'],
  }
}

include nginx_setup
