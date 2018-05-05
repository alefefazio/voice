#!/bin/bash
docker-compose -f docker/compose/test.yml run voice unittests.sh
exitcode=$?
docker-compose -f docker/compose/test.yml down
exit $exitcode
