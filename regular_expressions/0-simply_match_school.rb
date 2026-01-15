#!/usr/bin/env ruby
import = ARGV[0]
pattern = /\bSchool\b/
if import.match?(pattern)
  puts import
end

