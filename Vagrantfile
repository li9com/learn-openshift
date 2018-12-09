Vagrant.configure(2) do |config|
  config.vm.define "openshift" do |conf|
    conf.vm.box = "centos/7"
    conf.vm.network "private_network", ip: "172.24.0.11"
    conf.vm.hostname = 'openshift.example.com'
    conf.vm.provider "virtualbox" do |v|
      v.memory = 6000
      v.cpus = 2
    end
    conf.vm.provision "shell", inline: $lab_main
  end
end

$lab_main = <<SCRIPT
cat <<EOF > /etc/hosts
127.0.0.1   localhost localhost.localdomain
172.24.0.11 openshift.example.com openshift
EOF
yum install -y epel-release
yum install -y docker git vim
cat << EOF >/etc/docker/daemon.json
{
   "insecure-registries": [
     "172.30.0.0/16"
   ]
}
EOF
groupadd docker
usermod -s /bin/bash -aG docker vagrant

systemctl start --now docker

yum install -y centos-release-openshift-origin311
yum install -y origin-clients
oc cluster up \
   --public-hostname=openshift.172.24.0.11.nip.io \
   --routing-suffix=apps.172.24.0.11.nip.io
SCRIPT
