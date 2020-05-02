#!/usr/bin/env python                                                                                                                                                                                              
from gomatic import *

configurator = GoCdConfigurator(HostRestClient("localhost:8153"))
f = open("/var/lib/go-agent/config/autoregister.properties", "a")
f.write("agent.auto.register.resources=localhost\n")
f.write("agent.auto.register.key="+configurator.agent_auto_register_key+"\n")
f.close()
