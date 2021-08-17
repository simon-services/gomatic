#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact


configurator = GoCdConfigurator(HostRestClient("localhost:8153"))
pipeline = configurator \
    .ensure_pipeline_group("simon.services") \
    .ensure_replacement_of_pipeline("mbedtls") \
    .set_git_url("https://github.com/simon-services/mbedtls.git")

stage = pipeline.ensure_stage("build")
job_build = stage.ensure_job("cmake")
job_build.ensure_resource("localhost")
job_build.add_task(ExecTask(['mkdir','build']))
job_build.add_task(ExecTask(['bash','-c','cd build && cmake .. && cmake --build .']))
job_build.add_task(ExecTask(['bash','-c','mkdir -p mbedtls/libs && cp -rf include mbedtls/ && rm -fv mbedtls/include/CMakeLists.txt']))
job_build.add_task(ExecTask(['bash','-c','cp -rf build/library/*.a mbedtls/libs/']))
job_build.add_task(ExecTask(['bash','-c','tar cfvz mbedtls.tar.gz mbedtls && rm -rf mbedtls']))
job_build.ensure_artifacts({
    Artifact.get_test_artifact("mbedtls.tar.gz","pkg")
})
configurator.save_updated_config()
