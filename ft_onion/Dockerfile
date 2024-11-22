FROM nginx:latest

RUN apt-get update && apt-get install -y openssh-server

RUN ssh-keygen -A
COPY ./sshd_config /etc/ssh/sshd_config
RUN echo "root:johnavar42Berlin" | chpasswd

EXPOSE 4242

CMD ["/usr/sbin/sshd", "-D"]
