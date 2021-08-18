#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact


configurator = GoCdConfigurator(HostRestClient("localhost:8153"))
pipeline = configurator \
    .ensure_pipeline_group("simon.services") \
    .ensure_replacement_of_pipeline("services-test") \
    .set_git_material(GitMaterial("https://github.com/simon-services/services.git",branch="main")) \
    .ensure_material(PipelineMaterial("mbedtls", "build")) \
    .ensure_material(PipelineMaterial("nng", "build"))

stage = pipeline.ensure_stage("build")
job_build = stage.ensure_job("meson")
job_build.ensure_resource("localhost")

job_build.add_task(ExecTask(['wget','https://raw.githubusercontent.com/nanomsg/nng/master/demo/reqrep/reqrep.c']))

job_build.add_task(ExecTask(['bash','-c','mkdir include && mkdir libs']))

job_build.add_task(FetchArtifactTask('mbedtls', 'build', 'cmake', FetchArtifactFile('pkg/mbedtls.tar.gz'), dest='./', artifactOrigin='gocd'))
job_build.add_task(ExecTask(['bash','-c','tar xfvz mbedtls.tar.gz']))

job_build.add_task(FetchArtifactTask('nng', 'build', 'cmake', FetchArtifactFile('pkg/nng.tar.gz'), dest='./', artifactOrigin='gocd'))
job_build.add_task(ExecTask(['bash','-c','tar xfvz nng.tar.gz']))

job_build.add_task(ExecTask(['bash','-c','cp -rf mbedtls/include/* include/']))
job_build.add_task(ExecTask(['bash','-c','cp -rf mbedtls/libs/* libs/']))

job_build.add_task(ExecTask(['bash','-c','cp -rf nng/include/* include/']))
job_build.add_task(ExecTask(['bash','-c','cp -rf nng/libs/* libs/']))

job_build.add_task(ExecTask(['bash','-c','meson build && cd build && ninja']))

job_build.ensure_artifacts({
    Artifact.get_test_artifact('build/req','services'),
    Artifact.get_test_artifact('build/rep','services')
})

configurator.save_updated_config()
