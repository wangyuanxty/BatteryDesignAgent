import pybamm, json, inspect
p = pybamm.ParameterValues('Chen2020')
out = {}
for k in ['Electrolyte conductivity [S.m-1]', 'Electrolyte diffusivity [m2.s-1]']:
    v = p[k]
    out[k + '::type'] = type(v).__name__
    if callable(v):
        try:
            out[k + '::sig'] = str(inspect.signature(v))
        except Exception as e:
            out[k + '::sig'] = 'no-sig ' + repr(e)
        try:
            out[k + '::val_298'] = v(298.15)
        except Exception as e:
            out[k + '::err1'] = repr(e)
        try:
            out[k + '::val_kw'] = v(T=298.15)
        except Exception as e:
            out[k + '::err2'] = repr(e)
    else:
        out[k + '::val'] = v
print(json.dumps(out, indent=1))
