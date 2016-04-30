===============================
socialgraph
===============================

.. image:: https://img.shields.io/pypi/v/socialgraph.svg
        :target: https://pypi.python.org/pypi/socialgraph

.. image:: https://img.shields.io/travis/rodsenra/socialgraph.svg
        :target: https://travis-ci.org/rodsenra/socialgraph

.. image:: https://readthedocs.org/projects/socialgraph/badge/?version=latest
        :target: https://readthedocs.org/projects/socialgraph/?badge=latest
        :alt: Documentation Status


Exercises with social networks and property graphs

* Free software: ISC license
* Documentation: https://socialgraph.readthedocs.org.


Setup
-----

This is needed to be done just once.

:: In the shell:

    pip install -r requirements.txt


Server
------

1) Start the server:

         cd scripts
         . ./setup_pythonpath.sh
         python server.py localhost 8800

 Expected output:

        * Running on http://localhost:8800/ (Press CTRL+C to quit)


2) Test the server:

        ./test_server.sh

 Expected output:

        HTTP/1.1 100 Continue

        HTTP/1.0 200 OK
        Content-Type: application/json
        Content-Length: 110
        Server: Werkzeug/0.11.2 Python/2.7.11
        Date: Sat, 30 Apr 2016 21:31:15 GMT

        {
          "committee": {
            "12448": [
              "40976432",
              "28904",
              "12448",
              "16544"
            ]
          }
        }


Jupyter
--------

* Jupyter Notebook exploring dataset extracted from Wikipedia and decorated with random topics.

:: Use:

    pip install -r requirements_dev.txt

    cd notebooks
    
    jupyter notebook


Point your browser to http://localhost:8888 and use shift-enter to execute the notebook cells.


Titan DB
---------

1. Start the titan db

        bin/titan.sh start

   Expected output:

        Forking Cassandra...
        Running `nodetool statusthrift`.. OK (returned exit status 0 and printed string "running").
        Forking Elasticsearch...
        Connecting to Elasticsearch (127.0.0.1:9300).. OK (connected to 127.0.0.1:9300).
        Forking Gremlin-Server...
        Connecting to Gremlin-Server (127.0.0.1:8182).... OK (connected to 127.0.0.1:8182).
        Run gremlin.sh to connect.

2. Start the gremlin shell

        ./bin/gremlin.sh

    Expected output:

                \,,,/
                 (o o)
        -----oOOo-(3)-oOOo-----
        plugin activated: aurelius.titan
        plugin activated: tinkerpop.server
        plugin activated: tinkerpop.utilities
        SLF4J: Class path contains multiple SLF4J bindings.
        SLF4J: Found binding in [jar:file:/usr/local/src/titan-1.0.0-hadoop1/lib/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]
        SLF4J: Found binding in [jar:file:/usr/local/src/titan-1.0.0-hadoop1/lib/logback-classic-1.1.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
        SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
        SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
        13:22:31 INFO  org.apache.tinkerpop.gremlin.hadoop.structure.HadoopGraph  - HADOOP_GREMLIN_LIBS is set to: /usr/local/src/titan-1.0.0-hadoop1/lib
        plugin activated: tinkerpop.hadoop
        plugin activated: tinkerpop.tinkergraph

3. Connect the shell with the server

        :remote connect tinkerpop.server conf/remote.yaml

    Expected output:

        ==>Connected - localhost/127.0.0.1:8182



4. Load a graphml into Titan DB

        graph = TitanFactory.open()
        graph.io(IoCore.graphml()).readGraph("/Users/rodsenra/r/projects/WorkCo/socialgraph/datasets/wiki.graphml")



Credits
---------

This code was originally created by Rodrigo Senra <rodsenra@gmail.com> .

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
