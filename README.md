# Tolk
Tolk exposes a JSON-RPC API to talk Modbus over RTU and is written in Python.

## Docker
A Dockerfile has been provided for running and testing Tolk and building the
documentation. In order to use it you've to build an image first:

```shell
$ docker-compose build
```

A [docker-compose.yml][docker-compose] has been provided for convenience.

## Tests
Tolk uses [Pytest][pytest]. Running the test stuite is easy:

```shell
$ docker-compose run tests
```

## Documentation
Documentation resides in docs/ and is written using Sphinx. The source of
documentation is located at docs/source. The builded docs are written to
docs/build.

```shell
$ docker-compose run docs
```
The generated docs are stored in `docs/build/`.

## License
This software is licensed under [Mozila Public License][mpl].
&copy; 2015 [Advanced Climate Systems][acs].

[acs]: http://advancedclimate.nl
[docker-compose]: docker-compose.yml
[mpl]: LICENSE
[pytest]: http://pytest.org/latest/
[sphinx]: http://sphinx-doc.org/
