#!/usr/bin/env python
#coding=utf-8


def decode_url(x):
    s = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    s_ord = {}
    for i in range(len(s)):
        s_ord[s[i]] = i
    
    dif = - s_ord[x[0]] + s_ord['h'] + len(s)
    res = []
    for i in x:
        if i == '.' or i == '/' or i == ':':
            res.append(i)
        else:
            res.append(s[ (s_ord[i] + dif) % len(s) ])
    return ''.join(res)


# Another shell script
#<(︶︿︶)>[~/桌面]:echo "1DD9://vv6yx2u.AA.w86/6yx2u/6EC2w/uEx28/MKKSKO/vy232701Eu7I27072.69N" |tr "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRST" "qrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#HTTP://BBMEDIA.QQ.COM/MEDIA/MUSIC/AUDIO/200804/BEIJINGHUANYINGNI.MP3

if __name__ == '__main__':
    url = '6IIE://00B327z.FF.1DB/B327z/12/3CI/PXQPRW/9Jz7A3.BES'
    
    # return - "http://bbmedia.qq.com/media/cd/ent/081027/kuaile.mp3"    
    print decode_url(url)
