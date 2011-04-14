# TODO split this out into modules so people can use them in their own puppet setup
# TODO These are a pretty disgusting example of sane puppet configs

stage { "first": before => Stage[packages] }
stage { "packages": before => Stage[main] }
class {
  "apt": stage => first;
  "zookeepr_packages": stage => packages;
}

class apt {
  exec { "apt_update":
    command => "/usr/bin/sudo aptitude update",
  }
}

class nginx {

  service { "nginx":
    ensure => running,
    require => Package["nginx"],
  }

  package { "nginx":
    ensure => installed,
  }

}


class zookeepr_packages {


  $packages = [ 'python-authkit', 'python-dnspython', 'python-imaging',
                'python-pastedeploy', 'python-pylons', 'python-setuptools',
                'inkscape', 'gnupg', 'mpage', 'ghostscript', 'graphviz',
                'git-core', 'python-flup'
  ]

  package { $packages:
    ensure => present,
  }
}

class zookeepr {
  include zookeepr_packages
  exec { "zookeepr_lca_config":
    creates => "/vagrant/zookeepr/config/lca_info.py",
    command => "/bin/cp /vagrant/zookeepr/config/lca_info.py.sample /vagrant/zookeepr/config/lca_info.py",
  }

  file { "/vagrant/setup-dir":
    ensure => directory,
  }

  exec { "zookeepr_python":
    creates     => '/vagrant/setup-dir/zookeepr.egg-link',
    environment => 'PYTHONPATH=/vagrant/setup-dir',
    command     => '/usr/bin/python setup.py develop --no-deps --install-dir=/vagrant/setup-dir',
    cwd         => '/vagrant',
    require     => File["/vagrant/setup-dir"],
  }

  exec { "zookeepr_config":
    creates     => '/vagrant/config.ini',
    environment => 'PYTHONPATH=/vagrant/setup-dir',
    command     => '/usr/bin/paster make-config zookeepr config.ini',
    cwd         => '/vagrant',
    require     => Exec['zookeepr_python'],
  }

  exec { "zookeepr_setup":
    creates     => '/vagrant/development.db',
    environment => 'PYTHONPATH=/vagrant/setup-dir',
    command     => '/usr/bin/paster setup-app config.ini',
    cwd         => '/vagrant',
    require     => Exec['zookeepr_config'],
  }
}
class zookeepr::fastcgi {
  include zookeepr
  include nginx

  exec { "nginx_user":
    unless  => "/bin/grep 'user vagrant' /etc/nginx.conf",
    command => "/bin/sed -e 's/user www-data/user vagrant/' /etc/nginx/nginx.conf > /etc/nginx/nginx.conf.tmp && mv /etc/nginx/nginx.conf.tmp /etc/nginx/nginx.conf",
    notify  => Service["nginx"],
    require => Package['nginx'],
  }

  file { "/etc/nginx/sites-enabled/default":
    source => '/vagrant/vagrant/files/nginx',
    notify => Service['nginx'],
    require => Package['nginx'],
  }

  file { "/vagrant/logs":
    ensure => directory,
    before => File['/etc/nginx/sites-enabled/default'],
  }

  exec { "reconf_upstart":
    command     => "/sbin/initctl reload-configuration",
    refreshonly => true,
  }

  file { "/etc/init/zookeepr.conf":
    source => '/vagrant/vagrant/files/upstart',
    notify => Exec['reconf_upstart'],
  }

  exec { "start_zookeepr":
    command     => "/usr/sbin/service zookeepr stop; /usr/bin/sleep 1; /usr/sbin/service zookeepr start",
    unless      => "/bin/ps auxw | /bin/grep -q [p]aster",
    require     => File["/etc/init/zookeepr.conf"],
  }
}

include apt
include zookeepr::fastcgi
