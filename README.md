# stealthrome
POC of a Chrome Browser Password Stealer

The script outputs the passwords like this
![image](./output.png)

In practice, you could exfiltrate the master key and the database file and do the decryption locally in your machine.
 The reason we create copy of the files is because they're locked since they're accessed by the Chrome process. You could kill it if you don't want to drop any files.
