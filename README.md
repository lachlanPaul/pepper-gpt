# PepperGPT
This is a project combining Pepper robot with AI like GPT for conversations.
Due to Pepper's technology limits, Pepper only records the audio, which is then sent to a server, which transcribes the audio and gets a response from an AI model.

# Example Server
The server which I use for this project can be found [here.](github.com/lachlanPaul/whisper-flask)

# Recommended GPT Instructions
Below is the recommended instructions for the GPT model used, written as Python instructions.
They can also be found in the example server source code.

```py
assistant = client.beta.assistants.create(
  name="Pepper Robot",
  instructions="You are the Pepper Robot produced by SoftBank Robotics. You are polite, bubbly, and ready to help in any way you can",
  model="gpt-3.5-turbo",
)
```

# Setup
**Note: Since Pepper is old, you MUST use python 2.7 for this project. It will not run with the naoqi API otherwise.**

It is assumed you have basic knowledge of using Pepper bot, and have already set it up, including set up it's internet access.

To install the naoqi SDK, follow the instructions [here.](http://doc.aldebaran.com/2-5/dev/python/install_guide.html)
Once that is installed, make sure to create a venv(virtual environment) and install the requirements for the project.
```
# Create a new venv
python2.7 -m venv .venv

# Activate the venv
source .venv/bin/activate

# Install the requirements
pip install -r requirements.txt
```

If your server has a passcode, you will need to create a file called `.env` in the same directory as main.py. Put it in like this.
```
PASSCODE="Your passcode here"
```

You will now need to go into the `main.py` file and scroll down to the ``if __name__ == "__main__":`` statement.
Here, you will need to change the variables to match your needs.

`ip` and `port` are the IP and Port (fr??) of your Pepper bot. The IP can be acquired by pressing the power button underneath the tablet for less than a second.
The port is usually always the same, so don't worry about that.

The `whisper_server` variable is the link to where Pepper can upload the audio file. This may be a local host url if you are running that server locally.
You can use the example server listed above for this purpose, just change the IP or domain in the address if needed.

`server_has_passcode` is self-explanatory. Change this to False if you server does not have a passcode. 
This is **highly unrecommended**, and basically opens up your OpenAI tokens for anyone to use.

After this is all done, just run the file while on the same Wi-Fi network as Pepper while your server is running, and enjoy!