# Puppet manifest to install and configure Nginx
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
    content => '<html>\n<head>\n<title>Hello World</title>\n</head>\n<body>\nHello World!\n</body>\n</html>\n',
    require => Package['nginx'],
  }

  file { '/etc/nginx/sites-available/default':
    ensure
