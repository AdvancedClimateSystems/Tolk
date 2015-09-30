# Tolk
Tolk exposes a JSON-RPC API to talk Modbus over RTU and is written in Python.

## Documentationk
Documentation resides in docs/ and is written using Sphinx. The source of
documentation is located at docs/source. The builded docs are written to
docs/build. We use [this][orangetux_sphinx] Docker image for building the docs.

```shell
docker run --rm -ti -v $(pwd)/docs:/docs orangetux/sphinx
```
The generated docs are stored in `docs/build/`.

## License
This software is licensed under [Mozila Public License][mpl].
&copy; 2015 [Advanced Climate Systems][acs].

[acs]: http://advancedclimate.nl
[mpl]: LICENSE
[sphinx]: http://sphinx-doc.org/
