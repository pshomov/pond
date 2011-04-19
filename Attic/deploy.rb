#!/usr/bin/env ruby
require 'optparse'
require 'fileutils'
require 'system_common.rb'
include FileUtils


def process_folder (src, dest)
  mkdir dest  
  Dir.foreach(src) do |script|
    if !script.starts_with?("\\.") && File.directory?(script)
      process_folder(File.join(src, script),File.join(dest, script))
    else
      if !script.starts_with?("\\.")
        if script.ends_with?("\\.erb")
          puts "processing #{script}"
          _s("erb #{src}/#{script} > #{dest}/#{script[0..-5]}")
        else
          puts "copying #{script}"
          cp (File.join(src,script), File.join(dest,script))
        end
      end
    end
  end
end

options = {}
options[:ssh_port] = 22
OptionParser.new do |opts|
  opts.banner = "Usage: deploy.rb [options]"

  opts.on("-p [PORT]", Integer, "port to ssh to") do |v|
    options[:ssh_port] = v
  end
end.parse!(ARGV)

if ENV["MONO_VERSION"].nil? 
  puts red("MONO_VERSION not specified")
  exit 2
end
if ENV["MONO_XSP_VERSION"].nil? 
  puts red("MONO_XSP_VERSION not specified")
  exit 2
end
if ENV["LIBGDI_VERSION"].nil? 
  puts red("LIBGDI_VERSION not specified")
  exit 2
end

target = ARGV[0]
script_folder = File.dirname(__FILE__)
tmp_location = File.join(script_folder, "../tmp")
remove_dir tmp_location, :force => true
process_folder script_folder, tmp_location
_s "ssh -p #{options[:ssh_port]} -i ~/.ssh/root_id_rsa root@#{target} \"rm -rdf machine_scripts\""
_s "scp -P #{options[:ssh_port]} -i ~/.ssh/root_id_rsa -r ../tmp root@#{target}:~/machine_scripts"
_s "ssh -p #{options[:ssh_port]} -i ~/.ssh/root_id_rsa root@#{target} \"chmod +x machine_scripts/*.sh machine_scripts/*.rb; machine_scripts/fresh_machine.sh\""
