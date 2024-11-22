FROM nginx:alpine

RUN apk update && apk add --no-cache openssh \
	&& mkdir /var/run/sshd

COPY sshd_config /etc/ssh/sshd_config
RUN echo "root:ft_onion" | chpasswd \
	&& ssh-keygen -A

EXPOSE 4242

CMD ["/bin/sh", "-c", "nginx && /usr/sbin/sshd -D"]
