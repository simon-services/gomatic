#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact


configurator = GoCdConfigurator(HostRestClient("localhost:8153"))
pipeline = configurator \
    .ensure_pipeline_group("simon.services") \
    .ensure_replacement_of_pipeline("testing-deb") \
    .set_git_url("https://github.com/simon-services/testing-deb.git")


stage = pipeline.ensure_stage("deb")
job_deb = stage.ensure_job("build")
job_deb.ensure_resource("localhost")
job_deb.add_task(ExecTask(['make']))
job_deb.ensure_artifacts({
    Artifact.get_test_artifact("testing-0.0.1-amd64.deb","pkg")
})
configurator.save_updated_config()
