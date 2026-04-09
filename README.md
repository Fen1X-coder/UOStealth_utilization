# UOStealth_utilization

Welcome to my write-up on UOStealth, a program used with Ultima Online as a client assistant, or to be used in tandem with UOSteam in this case.

I cannot take full credit, as I used Google Gemini to assist with the process, but here is the result.

Resources:
  https://stealth.od.ua/ - UOStealth project main website.
  https://www.uosteam.com/ - UOSteam project main website.

Here is the breakdown:
Use UOStealth to create a 'headless' connection to your Ultima Online server. Point UOSteam to the localhost, providing a connection to the server via the Ultima Online client. This will allow you to run Python AND Steam scripts simotaneously.

You can run a Python looter script natively inside UOStealth. UOStealth will handle grabbing the items instantly at the packet level. You can then use UOStealth to launch your visual game window using UOSteam, giving you full access to your UOSteam hotkeys and macros and spellgrids etc.

______________________________________
Step 1: Connect UOStealth to Your Shard
First, we need to make sure UOStealth can log into the game on its own.
Open UOStealth and go to the Settings button (top right corner) and point it to the server's login port. (usually 2593)
Under Accounts on the main window (top center) click edit.
 -Type in your character or account name and hit the + button.
 -Fill in the Account and Password for that shard. 
   - Check "always select 1 1" if you have one character on the account, (2,3,4 respectively otherwise.)
 - Next to Shard, click edit.
   - Enter your real shard information (Name, Server IP, Port). Do not select UseProxy.
   - Select the correct client version. (can be located in Properties on the client file.)
   - Path to your Ultima Online installation folder.
 - Under "Selected Client:" click edit. Name it. Select the UOS.exe (UOSteam) file in the wherever that is installed. Leave nothing checked below. Click OK+(Save) button.
 - Back to the 'Shard Setup' window. Click Save then Close.
 - Back to 'Profiles Setup' window. Click Save then Close.
Hit Connect (top middle, next to Disconnect and Auto).
 - You want to see the text log show that you have successfully logged in (headless).
 - "Character "NAME" Connected." will be the message displayed.
You should see 'Connected' in green in the top right. As well as your stats.

_____________________________________
Step 2: Connect UOSteam to UOStealth
Secondly, we need to point UOSteam to UOStealth.
Now we tell UOSteam to stop trying to connect to the internet, and instead connect directly to UOStealth on your computer.
Open UOSteam (do not hit start yet).
 - Look at the Shard box where you would normally put the server IP.
 - Erase the real server IP and type in 127.0.0.1 (This is the universal IP address for "my local computer").
 - In the Port box, enter the exact Client Port number you found in UOStealth during Step 1 (e.g., 2593).

Once this step is complete, and you log in, you should see your character name as the Server list. I don't know why, but it is okay, proceed to character selection and you will successfully be logged in using UOSteam and all it has to offer, in addition to UOStealth, with its separate strings of scripts you can run simotaneously.

Please provide feedback as needed in the Repository.


I will provide scripts I worked on in the Repository as well.


- FEN1X-coder
