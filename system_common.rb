class String
  def starts_with?(characters)
      self.match(/^#{characters}/) ? true : false
  end
  def ends_with?(characters)
      self.match(/#{characters}$/) ? true : false
  end
end

def _s(command)
  puts(green(">>Launching #{command}"))
  system(command)
  if $? != 0
  	puts(red("Error running '#{command}'!"))
  	exit $?
  end
end

def colorize(text, color_code)
  "\e[#{color_code}m#{text}\e[0m"
end

def red(text); colorize(text, "31"); end
def green(text); colorize(text, "32"); end
