# Author: noraj
# Author website: https://rawsec.ml

require 'cinch' # gem install cinch
require 'digest'
require 'openssl'
require 'base64'
require 'pwned' # gem install pwned

def flag_part(num)
  flag = File.open('flag.txt', 'r').read()
  # Flag part size
  fps = flag.size / 3
  case num
  when 1
    flag[0...fps]
  when 2
    flag[fps...2*fps]
  when 3
    flag[2*fps..(-1)]
  end
  # flag_part(1)+flag_part(2)+flag_part(3) == flag => true
end

# anti-flood delay in second
D = 5.freeze

bot = Cinch::Bot.new do
  configure do |c|
    c.server   = ARGV[0].to_s
    c.port      = 6697
    c.ssl.use   = true
    c.nick     = "Apox"
  end

  # Global variables, let them empty
  challenge1_answer = {}
  challenge2_answer = {}
  challenge3_answer = {}

  on :connect do |m|
    bot.oper('OWw6tqI0BGbwFN1LuO8zuqao', 'chall')
  end

  on :private, /^!part1$/ do |m|
    sleep D
    m.user.refresh
    unless m.user.idle < D
      #m.reply "Hi #{m.user.nick}"
      # Random integer between 1 and 10000
      prng = Random.new
      rand_int = prng.rand(1..10000)
      # Pick random password
      passwd = IO.readlines('10k_most_common.txt')[rand_int].chomp
      #Save clear password in gobal variable
      challenge1_answer[m.user.user] = passwd
      # get hex value of the md5 hash of the password
      hash = Digest::MD5.hexdigest passwd
      # Insert a colon `:` every to char to get it more difficult to copy/paste manually
      hash = hash.scan(/.{1,2}/).join(':')
      m.reply "Crack this md5 hash: #{hash}, you have 3 seconds to answer"
      Timer(3, {shots: 1}) { m.reply "Time's up!"
                              challenge1_answer[m.user.user] = "" }
    end
  end

  on :private, /^!part1 -ans (.*)/ do |m, ans|
    if ans == challenge1_answer[m.user.user] and not ans.empty?
      m.reply 'Part 1 of the Flag: ' + flag_part(1)
    else
      #m.reply 'Too late or bad answer'
    end
  end

  on :private, /^!part2$/ do |m|
    sleep D
    m.user.refresh
    unless m.user.idle < D
      #m.reply "Hi #{m.user.nick}"
      message = 'Decipher this, you have 3 seconds to answer. '
      # random password
      prng = Random.new
      rand_int = prng.rand(1..10000)
      passwd = IO.readlines('10k_most_common.txt')[rand_int].chomp
      # Save clear password in gobal variable
      challenge2_answer[m.user.user] = passwd
      # init cipher
      cipher = OpenSSL::Cipher.new('camellia256')
      cipher.encrypt
      key = cipher.random_key
      iv = cipher.random_iv
      # cipher password
      encrypted = cipher.update(passwd) + cipher.final
      message += 'cipher: camellia256, '
      message += "key: #{Base64.encode64(key).chomp}, "
      message += "iv: #{Base64.encode64(iv).chomp}, "
      message += "encrypted: #{Base64.encode64(encrypted).chomp}"
      m.reply message
      Timer(3, {shots: 1}) { m.reply "Time's up!"
                              challenge2_answer[m.user.user] = "" }
    end
  end

  on :private, /^!part2 -ans (.*)/ do |m, ans|
    if ans == challenge2_answer[m.user.user] and not ans.empty?
      m.reply 'Part 2 of the Flag: ' + flag_part(2)
    else
      #m.reply 'Too late or bad answer'
    end
  end

  on :private, /^!part3$/ do |m|
    sleep D
    m.user.refresh
    unless m.user.idle < D
      #m.reply "Hi #{m.user.nick}"
      # random password
      prng = Random.new
      rand_int = prng.rand(1..10000)
      passwd = IO.readlines('10k_most_common.txt')[rand_int].chomp
      m.reply "Give me the number of times this password: #{passwd}, has been pwned using Pwned Passwords by Troy Hunt"
      # Check password pwnage count
      passwdcheck = Pwned::Password.new(passwd, { 'User-Agent' => 'SIGSEGV1-CTF-irc-challenge-password-pwn-count' })
      # Save password pwnage count in gobal variable
      challenge3_answer[m.user.user] = passwdcheck.pwned_count.to_s
      Timer(3, {shots: 1}) { m.reply "Time's up!"
                              challenge3_answer[m.user.user] = "" }
    end
  end

  on :private, /^!part3 -ans ([0-9]*)/ do |m, ans|
    if ans == challenge3_answer[m.user.user] and not ans.empty?
      m.reply 'Part 3 of the Flag: ' + flag_part(3)
    else
      #m.reply 'Too late or bad answer'
    end
  end

  on :private, /^!credit$/ do |m|
    sleep D
    m.user.refresh
    unless m.user.idle < D
      message = 'Challenge: IRC Bot, '
      message += 'Author: noraj from rawsec, '
      message += 'Author website: rawsec.ml'
      m.reply message
    end
  end

=begin
  on :private, /^!help$/ do |m|
    sleep D
    m.user.refresh
    unless m.user.idle < D
      m.reply 'List of available commands:'
      m.reply '!help => Display this help message'
      m.reply '!credit => Display challenge credit'
      m.reply '!part1 => Launch part 1 of the challenge'
      m.reply '!part1 -ans your_answer => Send your answer for part 1 of the challenge'
      m.reply '!part2 => Launch part 2 of the challenge'
      m.reply '!part2 -ans your_answer => Send your answer for part 2 of the challenge'
      m.reply '!part3 => Launch part 3 of the challenge'
      m.reply '!part3 -ans your_answer => Send your answer for part 3 of the challenge'
    end
  end
=end
end

bot.start
