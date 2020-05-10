#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact


configurator = GoCdConfigurator(HostRestClient("localhost:8153"))
pipeline = configurator \
    .ensure_pipeline_group("simon.services") \
    .ensure_replacement_of_pipeline("files-frontend") \
    .set_git_url("https://github.com/simon-services/files-frontend.git")

stage = pipeline.ensure_stage("tar")
job_deb = stage.ensure_job("web")
job_deb.ensure_resource("localhost")
job_deb.add_task(ExecTask(['make']))
job_deb.ensure_artifacts({
    Artifact.get_test_artifact("files-frontend.tar.gz","dist")
})
configurator.save_updated_config()
