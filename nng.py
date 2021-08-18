#!/usr/bin/env python
from gomatic import *
from gomatic.gocd.artifacts import Artifact


configurator = GoCdConfigurator(HostRestClient("localhost:8153"))
pipeline = configurator \
    .ensure_pipeline_group("simon.services") \
    .ensure_replacement_of_pipeline("nng") \
    .set_git_url("https://github.com/simon-services/nng.git") \
    .ensure_material(PipelineMaterial("mbedtls", "build"))

stage = pipeline.ensure_stage("build")
job_build = stage.ensure_job("cmake")
job_build.ensure_resource("localhost")
job_build.add_task(ExecTask(['mkdir','build']))
job_build.add_task(FetchArtifactTask("mbedtls", "build", "cmake", FetchArtifactFile("pkg/mbedtls.tar.gz"), dest="build", artifactOrigin="gocd"))
job_build.add_task(ExecTask(['bash','-c','cd build && tar xfvz mbedtls.tar.gz']))
job_build.add_task(ExecTask(['bash','-c','cd build && cmake -G Ninja -DMBEDTLS_ROOT_DIR=mbedtls/libs -DMBEDTLS_INCLUDE_DIR=mbedtls/include -DMBEDTLS_TLS_LIBRARY=mbedtls/libs/libmbedtls.a -DMBEDTLS_CRYPTO_LIBRARY=mbedtls/libs/libmbedcrypto.a -DMBEDTLS_X509_LIBRARY=mbedtls/libs/libmbedx509.a -DNNG_ENABLE_TLS=ON ..']))
job_build.add_task(ExecTask(['bash','-c','cd build && ninja']))
job_build.add_task(ExecTask(['bash','-c','mkdir -p nng/libs && cp -rf include nng/']))
job_build.add_task(ExecTask(['bash','-c','cp -f build/libnng.a nng/libs/']))
job_build.add_task(ExecTask(['bash','-c','tar cfvz nng.tar.gz nng && rm -rf nng']))
job_build.ensure_artifacts({
    Artifact.get_test_artifact("nng.tar.gz","pkg"),
    Artifact.get_test_artifact("build/src/tools/nngcat/nngcat","tools")
})
configurator.save_updated_config()
