# Run agent in server mode
server = true

data_dir = "/var/lib/consul"
log_level = "INFO"

# BOOTSTRAPPING and/or SINGLE NODE CLUSTER
# Requires server = true. A server configured with
# bootstrap_expect = n waits until n servers are available to
# bootstrap the cluster.
# Setting to 1 is equivalent to boostrap = true, turning on bootstrap
# mode. In bootstrap mode a server is allowed to elect itself as
# cluster leader. Only a single node can be in this mode. Used for
# bootstrappping a cluster, or to RUN A SINGLE NODE CLUSTER (not recommended)
# bootstrap = true

# Enable built-in web UI, by default on port 8500
# ui = true

# Address to which Consul binds client interfaces, by default allows
# only loopback connections.
# client_addr = "127.0.0.1"


# Security configuration, check first
# https://www.consul.io/docs/agent/encryption.html

# Gossip uses simmetric encryption, to generate a key use
# 'consul keygen'
# encrypt = "vOUi/EEEmdirT2W7AmKY/w=="

# RPC encryption requires a CA certificate and a certificate signed by
# that CA. All servers *MUST* have a certificate valid for
# server.<datacenter>.<domain>, for example CN = server.dc1.consul
# This is so that a compromised client with a client cert can not be
# used in server mode.
# cert_file = "/etc/consul.d/certs/consul_server_cert.pem"
# key_file = "/etc/consul.d/certs/consul_server_key.pem"
# ca_file = "/etc/consul.d/certs/CAcert.pem"
# verify_outgoing = true
# verify_server_hostname = true
# verify_incoming = true
