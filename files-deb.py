#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact


configurator = GoCdConfigurator(HostRestClient("localhost:8153"))
pipeline = configurator \
    .ensure_pipeline_group("simon.services") \
    .ensure_replacement_of_pipeline("files-deb") \
    .set_git_url("https://github.com/simon-services/files-deb.git") \
    .ensure_material(PipelineMaterial("files", "service")) \
    .ensure_material(PipelineMaterial("files-frontend", "tar"))

stage = pipeline.ensure_stage("deb")
job_deb = stage.ensure_job("build")
job_deb.ensure_resource("localhost")
job_deb.add_task(FetchArtifactTask("files", "service", "build", FetchArtifactFile("bin/files.linux.amd64"), dest="pkg", artifactOrigin="gocd"))
job_deb.add_task(FetchArtifactTask("files-frontend", "tar", "web", FetchArtifactFile("dist/files-frontend.tar.gz"), dest="pkg", artifactOrigin="gocd"))
job_deb.add_task(ExecTask(['bash','-c','mv pkg/files.linux.amd64 opt/simon.services/files/bin/files && chmod +x opt/simon.services/files/bin/fils']))
job_deb.add_task(ExecTask(['bash','-c','cd pkgs && tar xfvz files-frontend.tar.gz && rm -fv files-frontend.tar.gz && mv files-frontend/* opt/simon.services/files/webroot/ && rm -rf files-frontend && cd ../ && rm -rf pkg']))
job_deb.add_task(ExecTask(['make']))
job_deb.ensure_artifacts({
    Artifact.get_test_artifact("files-0.0.1-amd64.deb","pkg")
})
configurator.save_updated_config()

