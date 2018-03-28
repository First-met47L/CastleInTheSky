Task Name | bit Value | Description
:----:|:------:|:------:
Follow users| 0b00000001 (0x01) |Follow other users
Comment on posts made by others| 0b00000010 (0x02)| Comment on articles written by others
Write articles |0b00000100 (0x04) |Write original articles
Moderate comments made by others| 0b00001000 (0x08) |Suppress offensive comments made by others
Administration access |0b10000000 (0x80) | Administrative access to the site

***
##User roles 
User role |Permissions|Description
:---:|:---:|:---:
Anonymous |0b00000000 (0x00)| User who is not logged in. Read-only access to the application.
User |0b00000111 (0x07) |Basic permissions to write articles and comments and to follow other users. This is the default for new users.
Moderator| 0b00001111 (0x0f) |Adds permission to suppress comments deemed offensive or inappropriate.
Administrator | 0b11111111 (0xff)|Full access, which includes permission to change the roles of other users.