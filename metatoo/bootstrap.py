"""
Bootstrap the metatoo compiler by compiling the metatoo grammar
using a hand-translation of itself into peglet.
"""

import sys
from peglet import Parser, join

meta_grammar = r"""
main   =                      main_start
         _ rules !.
rules  = rule rules
       | 
rule   = id /=/ _ alts [.] _  rule_do
alts   =                      seq_start
         seq alts2
alts2  = [|] _ alts
       | 
seq    = token seq
       |                      seq_end

token  = [{] qchars [}] _     join tok_qchars
       | [/] xchars [/] _     join tok_xchars
       | id                   tok_id
       | [:] id               tok_primitive

qchars = qchar qchars
       | 
qchar  = ([^}])

xchars = xchar xchars
       | 
xchar  = /(\\.|[^\/])/

id     = ([a-zA-Z_]\w*) _
_      = \s*
"""

def main_start():
    return ("# This file was generated by metatoo; you probably shouldn't edit it.\n"
            "import metalib, re\n"
            "def meta(text):\n"
            "  pos, vals = parse_main(text, 0, ())\n"
            "  if pos != len(text): raise Exception('Failed', pos)\n"
            "  return ''.join(vals)\n")
def rule_do(name, *body):
    return ("def parse_%s(text, start_pos, start_vals):\n"
            "%s"
            "  return None, None\n"
            % (name, ''.join(body)))
def seq_start():
    return ("  while True:\n"
            "    pos, vals = start_pos, start_vals\n")
def seq_end():
    return ("    return pos, vals\n")
def tok_qchars(*chars):
    return ("    vals += (%r,)\n"
            % ''.join(chars))
def tok_xchars(*chars):
    return ("    m = re.match(%r, text[pos:])\n"
            "    if not m: break\n"
            "    pos, vals = pos + m.end(), vals + m.groups()\n"
            % ''.join(chars))
def tok_id(name):
    return ("    pos, vals = parse_%s(text, pos, vals)\n"
            "    if pos is None: break\n"
            % name)
def tok_primitive(name):
    return ("    vals = metalib.%s(vals)\n"
            % name)

def meta(text):
    return Parser(meta_grammar, **globals())(text)

with open('metatoo.metatoo') as f:
    sys.stdout.write(''.join(meta(f.read())))
#. # This file was generated by metatoo; you probably shouldn't edit it.
#. import metalib, re
#. def meta(text):
#.   pos, vals = parse_main(text, 0, ())
#.   if pos != len(text): raise Exception('Failed', pos)
#.   return ''.join(vals)
#. def parse_main(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     vals += ("# This file was generated by metatoo; you probably shouldn't edit it.",)
#.     vals = metalib.nl(vals)
#.     vals += ('import metalib, re',)
#.     vals = metalib.nl(vals)
#.     vals += ('def meta(text):',)
#.     vals = metalib.nl(vals)
#.     vals += ('  pos, vals = parse_main(text, 0, ())',)
#.     vals = metalib.nl(vals)
#.     vals += ("  if pos != len(text): raise Exception('Failed', pos)",)
#.     vals = metalib.nl(vals)
#.     vals += ("  return ''.join(vals)",)
#.     vals = metalib.nl(vals)
#.     pos, vals = parse__(text, pos, vals)
#.     if pos is None: break
#.     pos, vals = parse_rules(text, pos, vals)
#.     if pos is None: break
#.     return pos, vals
#.   return None, None
#. def parse_rules(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     pos, vals = parse_rule(text, pos, vals)
#.     if pos is None: break
#.     pos, vals = parse_rules(text, pos, vals)
#.     if pos is None: break
#.     return pos, vals
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     return pos, vals
#.   return None, None
#. def parse_rule(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     pos, vals = parse_id(text, pos, vals)
#.     if pos is None: break
#.     m = re.match('=', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse__(text, pos, vals)
#.     if pos is None: break
#.     vals += ('def parse_',)
#.     vals = metalib.swap(vals)
#.     vals += ('(text, start_pos, start_vals):',)
#.     vals = metalib.nl(vals)
#.     pos, vals = parse_alts(text, pos, vals)
#.     if pos is None: break
#.     m = re.match('\\.', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse__(text, pos, vals)
#.     if pos is None: break
#.     vals += ('  return None, None',)
#.     vals = metalib.nl(vals)
#.     return pos, vals
#.   return None, None
#. def parse_alts(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     vals += ('  while True:',)
#.     vals = metalib.nl(vals)
#.     vals += ('    pos, vals = start_pos, start_vals',)
#.     vals = metalib.nl(vals)
#.     pos, vals = parse_seq(text, pos, vals)
#.     if pos is None: break
#.     pos, vals = parse_alts2(text, pos, vals)
#.     if pos is None: break
#.     return pos, vals
#.   return None, None
#. def parse_alts2(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     m = re.match('\\|', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse__(text, pos, vals)
#.     if pos is None: break
#.     pos, vals = parse_alts(text, pos, vals)
#.     if pos is None: break
#.     return pos, vals
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     return pos, vals
#.   return None, None
#. def parse_seq(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     pos, vals = parse_token(text, pos, vals)
#.     if pos is None: break
#.     pos, vals = parse_seq(text, pos, vals)
#.     if pos is None: break
#.     return pos, vals
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     vals += ('    return pos, vals',)
#.     vals = metalib.nl(vals)
#.     return pos, vals
#.   return None, None
#. def parse_token(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     m = re.match('{', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse_qchars(text, pos, vals)
#.     if pos is None: break
#.     m = re.match('}', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse__(text, pos, vals)
#.     if pos is None: break
#.     vals += ('    vals += (',)
#.     vals = metalib.swap(vals)
#.     vals = metalib.quote(vals)
#.     vals += (',)',)
#.     vals = metalib.nl(vals)
#.     return pos, vals
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     m = re.match('\\/', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse_xchars(text, pos, vals)
#.     if pos is None: break
#.     m = re.match('\\/', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse__(text, pos, vals)
#.     if pos is None: break
#.     vals += ('    m = re.match(',)
#.     vals = metalib.swap(vals)
#.     vals = metalib.quote(vals)
#.     vals += (', text[pos:])',)
#.     vals = metalib.nl(vals)
#.     vals += ('    if not m: break',)
#.     vals = metalib.nl(vals)
#.     vals += ('    pos, vals = pos + m.end(), vals + m.groups()',)
#.     vals = metalib.nl(vals)
#.     return pos, vals
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     pos, vals = parse_id(text, pos, vals)
#.     if pos is None: break
#.     vals += ('    pos, vals = parse_',)
#.     vals = metalib.swap(vals)
#.     vals += ('(text, pos, vals)',)
#.     vals = metalib.nl(vals)
#.     vals += ('    if pos is None: break',)
#.     vals = metalib.nl(vals)
#.     return pos, vals
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     m = re.match('%', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse_id(text, pos, vals)
#.     if pos is None: break
#.     vals += ('    vals = metalib.',)
#.     vals = metalib.swap(vals)
#.     vals += ('(vals)',)
#.     vals = metalib.nl(vals)
#.     return pos, vals
#.   return None, None
#. def parse_qchars(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     m = re.match('([^}])', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse_qchars(text, pos, vals)
#.     if pos is None: break
#.     vals = metalib.cat(vals)
#.     return pos, vals
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     vals += ('',)
#.     return pos, vals
#.   return None, None
#. def parse_xchars(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     m = re.match('(\\\\.|[^\\/])', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse_xchars(text, pos, vals)
#.     if pos is None: break
#.     vals = metalib.cat(vals)
#.     return pos, vals
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     vals += ('',)
#.     return pos, vals
#.   return None, None
#. def parse_id(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     m = re.match('([a-zA-Z_]\\w*)', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     pos, vals = parse__(text, pos, vals)
#.     if pos is None: break
#.     return pos, vals
#.   return None, None
#. def parse__(text, start_pos, start_vals):
#.   while True:
#.     pos, vals = start_pos, start_vals
#.     m = re.match('\\s*', text[pos:])
#.     if not m: break
#.     pos, vals = pos + m.end(), vals + m.groups()
#.     return pos, vals
#.   return None, None
