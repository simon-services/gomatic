#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact


configurator = GoCdConfigurator(HostRestClient("localhost:8153"))
pipeline = configurator \
    .ensure_pipeline_group("simon.services") \
    .ensure_replacement_of_pipeline("reload") \
    .set_git_url("https://github.com/simon-services/gomatic.git")


stage = pipeline.ensure_stage("reload")
job_reload = stage.ensure_job("pipelines")
job_reload.ensure_resource("localhost")
job_reload.add_task(ExecTask(['make']))
configurator.save_updated_config()
