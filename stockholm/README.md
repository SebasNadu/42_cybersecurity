# Stockholm Ransomware Emulator

## About Ransomware

Ransomware is a type of malicious software designed to block access to a system or encrypt its data until a ransom is paid. It typically spreads through phishing emails, malicious links, or vulnerabilities in software.

### Inspiration: WannaCry

The Stockholm emulator takes inspiration from the infamous WannaCry ransomware. WannaCry leveraged the EternalBlue exploit to spread rapidly, encrypting files and demanding Bitcoin payment for decryption. The attack highlighted the importance of robust cybersecurity measures worldwide.

This project serves as an educational tool to understand ransomware mechanics, focusing on file encryption and decryption processes within a controlled environment.

---

## How to Run the Stockholm Emulator

### Requirements

- Docker installed on your system.
- Basic familiarity with Docker commands.

### Build and Run the Docker Container

1. Clone this repository and navigate to its directory:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Copy folders to attack (Desktop, Documents, and Downloads) into `./infection`. Build and start the Docker container:

```Bash
make all
or
make
```

### Execute the attack and free the files from the host

1. Encrypt the files inside `./infection`:

```Bash
 make encrypt
```

2. Decrypt the files inside `./infection`:

```Bash
 make decrypt KEY=key
```

### Execute the attack and free the files from the container

1. Access the running container:

```Bash
 docker exec -it stockholm /bin/sh
```

2. Navigate to HOME:

```Bash
 cd ~
```

3. Encrypt the files inside `./infection`:

```Bash
 python3 app/stockholm.py
```

4. Decrypt the files inside `./infection`:

```bash
 python3 app/stockholm.py -r key
```

---

### Encryption Keys

The program uses two keys defined in the `.env` file:

- **MASTER_KEY**: A human-readable string that serves as the seed for generating the final encryption key. In this example:

  ```
  MASTER_KEY="This is Stockholm!"
  ```

  The `MASTER_KEY` is converted into Base64 format and padded with null bytes (`\0`) until it reaches a length of 32 bytes. This process ensures compatibility with the encryption algorithm.

- **SECRET_KEY**: The actual key used for encryption and decryption. It is derived from the `MASTER_KEY` and is directly used as input for the cryptographic operations. Example:

  ```
  SECRET_KEY="VGhpcyBpcyBTdG9ja2hvbG0hAAAAAAAA"
  ```

The `SECRET_KEY` can be passed to the program as an argument to decrypt the files in the target directory.
