import re

l = [
	('a', 'r'),
	('q', 'u'),
	('u', 's'),
	('d', 'a'),
	('n', 'e'),
	('p', 'i'),
	('x', 'd'),
	('f', 'y'),
	('v', 'k'),
	('s', 't'),
	('l', 'n'),
	('z', 'g'),
	('g', 'l'),
	('w', 'w'),
	('nj', 'br'),
	('to', 'ic'),
	('zx', 'kn'),
	('yb', 'th'),
	('ow', 'in'),
	('wr', 'an'),
	('nw', 'sa'),
	('tj', 'id'),
	('ki', 'wa'),
	('sd', 'of'),
	('od', 'is'),
	('bg', 'up'),
	('lv', 'ge'),
	('xq', 'at'),
	('jo', 'to'),
	('om', 'we'),
	('ms', 'nt'),
	('yx', 'sn'),
	('by', 'er'),
	('cd', 'ed'),
	('ac', 'ou'),
	('dl', 'gh'),
	('ws', 'll'),
	('qs', 'un'),
	('ci', 'ow'),
	('zw', 'it'),
	('ad', 'no'),
	('aw', 'my'),
	('cz', 'on'),
	('sn', 'wh'),
	('pr', 'pe'),
	('jy', 're'),
	('qn', 'li'),
	('qo', 'tt'),
	('uo', 'le'),
	('hn', 'lo'),
	('kr', 'gh'),
	('aq', 'wi'),
	('wa', 'di'),
	('sb', 'al'),
	('eh', 'ab'),
	('nc', 'fo'),
	('ld', 'ta'),
	('cm', 'ss'),
	('mq', 'ne'),
	('sq', 'ti'),
	('kt', 'me'),
	('fz', 'bu'),
	('rq', 'su'),
	('uc', 'ch'),
	('yu', 'mu'),
	('tt', 'la'),
	('no', 'te'),
	('ef', 'rt'),
	('iq', 'ad'),
	('oe', 'pr'),
	('fn', 'ob'),
	('yh', 'ly'),
	('ij', 'yo'),
	('em', 'do'),
	('zk', 'ea'),
	('xh', 'co'),
	('ej', 'be'),
	('ea', 'ns'),
	('ex', 've'),
	('sg', 'mo'),
	('lo', 'rs'),
	('gz', 'ks'),
	('ha', 'mi'),
	('ao', 'nd'),
	('jd', 'st'),
	('xp', 'ke'),
	('bt', 'so'),
	('fd', 'od'),
	('rc', 'uc'),
	('uq', 'es'),
	('vt', 'rp'),
	('ol', 'en'),
	('xa', 'cy'),
	('ya', 'ho'),
	('zp', 'fr'),
	('xx', 'om'),
	('sp', 'wo'),
	('sv', 'sh'),
	('qb', 'na'),
	('xg', 'op'),
	('sw', 'ok'),
	('ba', 'tl'),
	('mw', 'ng'),
	('qc', 'la'),
	('zo', 'te'),
	('mu', 'ot'),
	('zv', 'he'),
	('Vp', 'io')
]

content = open('bookbrackets.enc', 'r').read()

for i in l:
	content = re.sub('\[' + i[0] + '\]', i[1], content, 0, re.I)

print(content)
