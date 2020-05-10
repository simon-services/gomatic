#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact


configurator = GoCdConfigurator(HostRestClient("localhost:8153"))
pipeline = configurator \
    .ensure_pipeline_group("simon.services") \
    .ensure_replacement_of_pipeline("files") \
    .set_git_url("https://github.com/simon-services/files.git")

stage = pipeline.ensure_stage("service")
job_deb = stage.ensure_job("build")
job_deb.ensure_resource("localhost")
job_deb.add_task(ExecTask(['make','build']))
job_deb.ensure_artifacts({
    Artifact.get_test_artifact("files.linux.amd64","bin")
})
configurator.save_updated_config()
