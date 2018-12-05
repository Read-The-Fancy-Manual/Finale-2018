#!/usr/bin/env ruby

# Author: noraj
# Author website: https://rawsec.ml

require 'cinch' # gem install cinch
require 'openssl'
require 'base64'
require 'curb' # gem install curb
require 'pwned' # gem install pwned

bot = Cinch::Bot.new do |boti|
    configure do |c|
        c.server    = "172.17.0.1"
        c.port      = 6697
        c.ssl.use   = true
        c.nick      = "noraj_501v3r"
    end

    # be ready to talk to noraj_bot
    challbot  = Cinch::Target.new("Apox", boti)
    # be ready to talk to you, to get flag back
    player  = Cinch::Target.new("noraj", boti)

    # run bot, example for challenge 1: "send_bot 1"
    on :private, /^send_bot ([0-9])/ do |m, num|
        challbot.send("!part#{num}")
    end

    # solving challenge part 1
    on :private, /^Crack this md5 hash: ((?:[a-f0-9]{2}:){15}[a-f0-9]{2}), you have [0-9]+ seconds to answer$/ do |m, md5_hash|
        # removing ':'
        md5_hash.gsub!(':', '')
        # request to hashes.org API, limited to 20 requests/min and need an account
        key = "CENSORED"
        hostname = "https://hashes.org/api.php?act=REQUEST&key=#{key}&hash=#{md5_hash}"
        c = Curl::Easy.new(hostname) do |curl|
            curl.headers['Referer'] = 'https://hashes.org/'
        end
        c.perform
        # result looks like {"REQUEST":"FOUND", "e252a5167841b3d3a28e9030615964fa": {"plain":"tango","hexplain":"74616e676f","algorithm":"MD5PLAIN"}}
        answer = c.body_str.match(/"plain":"(.*)","hex/).captures[0]
        m.reply "!part1 -ans #{answer}"
    end

    # solving challenge part 2
    on :private, /^Decipher this, you have [0-9]+ seconds to answer. cipher: camellia256, key: ((?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?), iv: ((?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?), encrypted: ((?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?)$/ do |m, k, i, e|
        c2_encrypted = Base64.decode64(e)
        # init cipher
        decipher = OpenSSL::Cipher.new('camellia256')
        decipher.decrypt
        # decipher password
        decipher.key = Base64.decode64(k)
        decipher.iv = Base64.decode64(i)
        passwd = decipher.update(c2_encrypted) + decipher.final
        m.reply "!part2 -ans #{passwd}"
    end

    # solving challenge part 3
    on :private, /^Give me the number of times this password: (.*), has been pwned using Pwned Passwords by Troy Hunt$/ do |m, pwd|
        passwdcheck = Pwned::Password.new(pwd, { 'User-Agent' => 'SIGSEGV1-CTF-irc-challenge-password-pwn-count' })
        m.reply "!part3 -ans #{passwdcheck.pwned_count}"
    end

    # sending the flag back to player
    on :private, /flag/i do |m|
        player.send(m.message)
    end
end

bot.start
