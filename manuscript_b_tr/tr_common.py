"""Türkçe sürümler için ortak biçimlendirme: ondalık virgül, binlik nokta, yüzde işareti önde."""


def num(x, d=2):
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".").replace("-", "−")


n = lambda x: num(x, 0)
f1 = lambda x: num(x, 1)
f2 = lambda x: num(x, 2)
f3 = lambda x: num(x, 3)
pct = lambda x, d=0: "%" + num(100 * x, d)
pp2 = lambda x: num(100 * x, 2)
pp3 = lambda x: num(100 * x, 3)


def fp(p):
    return "< 0,001" if p < 0.001 else "= " + num(p, 3)


ci = lambda v, d=2: f"{num(v[0], d)} ile {num(v[1], d)}"

ROLE_TR = {"Ball handler": "Top taşıyıcı", "Wing/forward": "Kanat/forvet", "Interior big": "İç uzun",
           "Rim protector": "Pota koruyucu", "Wing": "Kanat", "Stretch forward": "Açılan forvet"}
WORD_TR = {4: "dört", 5: "beş", 6: "altı", 7: "yedi"}
