#!/usr/bin/env ruby

require 'system_common.rb'

script_folder = File.dirname(__FILE__)
/etc/init.d/apache2 stop
update-rc.d apache disable
update-rc.d nginx enable
_s "cp #{script_folder}/default /etc/nginx/sites-enabled/default"
_s "/etc/init.d/nginx restart"