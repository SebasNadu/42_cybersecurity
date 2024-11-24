FROM python:3.13-alpine

RUN apk update && apk add --no-cache openssh \
	&& mkdir /var/run/sshd

COPY sshd_config /etc/ssh/sshd_config
RUN echo "root:stockholm" | chpasswd \
	&& ssh-keygen -A

EXPOSE 22

CMD ["/bin/sh", "-c", "/usr/sbin/sshd -D"]

