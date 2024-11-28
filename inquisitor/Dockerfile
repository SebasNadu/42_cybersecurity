FROM python:3

RUN apt-get -y update && apt-get upgrade -y \
	&& apt-get install -y openssh-server \
	libcap-dev \
	net-tools \
	arping \
	iputils-ping \
	vim \
	tcpdump \
	curl \
	iproute2 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/inquisitor

COPY ../volumes/inquisitor/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config \
	&& echo "root:root" | chpasswd \
	&& mkdir -p /run/sshd \
	&& ssh-keygen -A


EXPOSE 2121


CMD ["/usr/sbin/sshd", "-D"]
