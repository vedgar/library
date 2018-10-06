import tokenize, io, types, parser, symbol, collections, token, ast


class Token(types.SimpleNamespace):
    def __str__(self):
        return '{}{!r}'.format(self.vrsta, self.sadržaj)


def tokeni(ulaz):
    for token in tokenize.tokenize(io.BytesIO(ulaz.encode('utf8')).readline):
        t = Token()
        t.kod = token.type
        t.vrsta_kod = token.exact_type
        t.tip = tokenize.tok_name[token.type]
        t.vrsta = tokenize.tok_name[token.exact_type]
        t.sadržaj = token.string
        t.redak, t.stupac = token.start
        t.kraj_redak, t.kraj_stupac = token.end
        t.linija = token.line
        if t.tip not in {'ENCODING', 'ENDMARKER'}:
            yield t


def leksička_analiza(ulaz):
    try:
        for token in tokeni(ulaz): print(token)
    except tokenize.TokenError:
        print('Greška: nezavršen ulaz')


def uvrsti_simbole(stablo):
    korijen, *podstabla = stablo
    if korijen in symbol.sym_name:
        pravilo = [symbol.sym_name[korijen]]
        pravilo.extend(map(uvrsti_simbole, podstabla))
        return pravilo
    elif korijen in token.tok_name:
        sadržaj, = podstabla
        return token.tok_name[korijen] + ':' + sadržaj


def stablo_parsiranja(ulaz):
    for funkcija in parser.expr, parser.suite:
        try: stablo = funkcija(ulaz).tolist()
        except SyntaxError as greška: zadnja_greška = greška
        else:
            if stablo[-2:] == [[token.NEWLINE, ''], [token.ENDMARKER, '']]:
                del stablo[-2:]
            return uvrsti_simbole(stablo)
    poruka, (izvor, broj_linije, stupac, linija) = zadnja_greška.args
    print(linija + '^'.rjust(stupac) + ': greška')


def uvuci(vrijednost, ime=None, razina=0, uvlaka=' '*4, margina=80):
    def izbaci(t):
        if isinstance(t, ast.AST): return ast.dump(t)
        elif t is None: return 'None'
    početak = prefiks = uvlaka * razina
    završetak = ',' if razina else ''
    if ime is not None: početak += ime + ' = '
    if isinstance(vrijednost, ast.AST):
        jedna = početak + ast.dump(vrijednost) + ','
        if len(jedna) <= margina: print(jedna)
        else:
            print(početak + type(vrijednost).__name__ + '(')
            for dio in vrijednost._fields:
                uvuci(getattr(vrijednost, dio), dio, razina + 1)
            print(prefiks + ')' + završetak)
    elif isinstance(vrijednost, list):
        jedna = početak + '[' + ', '.join(map(izbaci, vrijednost)) + '],'
        if len(jedna) <= margina: print(jedna)
        else:
            print(početak + '[')
            for dio in vrijednost:
                uvuci(dio, None, razina + 1)
            print(prefiks + ']' + završetak)
    elif isinstance(vrijednost, (str, int)) or vrijednost is None:
        print(početak + repr(vrijednost) + završetak)
    else:
        raise TypeError('Nepoznat tip od {}'.format(vrijednost))


def apstraktno_sintaksno_stablo(ulaz):
    for mod in 'eval', 'single', 'exec':
        try: stablo = ast.parse(ulaz, '<ulaz>', mod)
        except SyntaxError as greška: zadnja_greška = greška
        else:
            t = stablo.body
            uvuci(t)
            return t
    poruka, (izvor, broj_linije, stupac, linija) = zadnja_greška.args
    if linija is None: linija = ulaz.splitlines()[broj_linije - 1] + '\n'
    print(linija + '^'.rjust(stupac) + ': ' + poruka)
