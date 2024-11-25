FROM python:3.13-alpine

RUN apk add --no-cache openssh \
	&& mkdir /var/run/sshd \
	&& echo "root:stockholm" | chpasswd \
	&& ssh-keygen -A

COPY sshd_config /etc/ssh/sshd_config

EXPOSE 22

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/usr/sbin/sshd", "-D"]
